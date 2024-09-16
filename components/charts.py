import base64
import io
from copy import deepcopy

import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pythermalcomfort.models import pmv
from pythermalcomfort.utilities import v_relative, clo_dynamic
from pythermalcomfort.psychrometrics import psy_ta_rh
from scipy import optimize

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, Models
from utils.website_text import TextHome
import matplotlib

matplotlib.use("Agg")


def chart_selector(selected_model: str):
    list_charts = deepcopy(Models[selected_model].value.charts)
    list_charts = [chart.name for chart in list_charts]
    drop_down_chart_dict = {
        "id": ElementsIDs.chart_selected.value,
        "question": TextHome.chart_selection.value,
        "options": list_charts,
        "multi": False,
        "default": list_charts[0],
    }

    return generate_dropdown_inline(
        drop_down_chart_dict, value=drop_down_chart_dict["default"], clearable=False
    )


# fig example
def t_rh_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    for pmv_limit in pmv_limits:
        for rh in np.arange(0, 110, 10):

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=rh,
                        met=inputs[ElementsIDs.met_input.value],
                        clo=clo_d,
                        wme=0,
                        standard=model,
                        limit_inputs=False,
                    )
                    - pmv_limit
                )

            temp = optimize.brentq(function, 10, 40)
            results.append(
                {
                    "rh": rh,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )
    df = pd.DataFrame(results)
    f, axs = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
    t1 = df[df["pmv_limit"] == pmv_limits[0]]
    t2 = df[df["pmv_limit"] == pmv_limits[1]]
    axs.fill_betweenx(
        t1["rh"], t1["temp"], t2["temp"], alpha=0.5, label=model, color="#7BD0F2"
    )
    axs.scatter(
        inputs[ElementsIDs.t_db_input.value],
        inputs[ElementsIDs.rh_input.value],
        color="red",
    )
    axs.set(
        ylabel="RH (%)",
        xlabel="Temperature (°C)",
        ylim=(0, 100),
        xlim=(10, 40),
    )
    axs.legend(frameon=False).remove()
    axs.grid(True, which="both", linestyle="--", linewidth=0.5)
    axs.spines["top"].set_visible(False)
    axs.spines["right"].set_visible(False)
    plt.tight_layout()

    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Heat stress chart",
        py=0,
    )


def t_hr_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )

    current_tdb = inputs[ElementsIDs.t_db_input.value]
    current_rh = inputs[ElementsIDs.rh_input.value]
    psy_data = psy_ta_rh(current_tdb, current_rh)

    for pmv_limit in pmv_limits:
        for rh in np.arange(10, 110, 10):
            psy_data_rh = psy_ta_rh(current_tdb, rh)

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=rh,
                        met=inputs[ElementsIDs.met_input.value],
                        clo=clo_d,
                        wme=0,
                        standard=model,
                        limit_inputs=False,
                    )
                    - pmv_limit
                )

            temp = optimize.brentq(function, 10, 40)
            results.append(
                {
                    "rh": rh,
                    "hr": psy_data_rh["hr"] * 1000,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )

    df = pd.DataFrame(results)

    fig, ax = plt.subplots(figsize=(8, 6))

    for rh in np.arange(10, 110, 10):
        temp_range = np.arange(10, 40, 1)
        hr_values = [psy_ta_rh(t, rh)["hr"] * 1000 for t in temp_range]
        ax.plot(temp_range, hr_values, color="grey", linestyle="--")

    t1 = df[df["pmv_limit"] == pmv_limits[0]]
    t2 = df[df["pmv_limit"] == pmv_limits[1]]
    ax.fill_betweenx(t1["hr"], t1["temp"], t2["temp"], alpha=0.5, color="#7BD0F2")

    ax.scatter(
        current_tdb, psy_data["hr"] * 1000, color="red", edgecolor="black", s=100
    )

    ax.set_xlabel("Dry-bulb Temperature (°C)", fontsize=14)
    ax.set_ylabel("Humidity Ratio (g_water/kg_dry_air)", fontsize=14)
    ax.set_xlim(10, 40)
    ax.set_ylim(0, 30)

    label_text = (
        f"t_db: {current_tdb:.1f} °C\n"
        f"rh: {current_rh:.1f} %\n"
        f"Wa: {psy_data['hr'] * 1000:.1f} g_w/kg_da\n"
        f"twb: {psy_data['t_wb']:.1f} °C\n"
        f"tdp: {psy_data['t_dp']:.1f} °C\n"
        f"h: {psy_data['h'] / 1000:.1f} kJ/kg"
    )

    ax.text(
        0.05,
        0.95,
        label_text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.6),
    )

    plt.tight_layout()

    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")

    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Psychrometric chart",
        py=0,
    )
