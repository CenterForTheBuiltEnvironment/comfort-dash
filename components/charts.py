import math
import numpy as np
import pandas as pd
from pythermalcomfort.models import pmv, cooling_effect, two_nodes
from pythermalcomfort.utilities import v_relative, clo_dynamic, units_converter
from scipy import optimize

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import (
    ElementsIDs,
    Models,
    Functionalities,
    UnitSystem,
    UnitConverter,
)
from utils.website_text import TextHome
import matplotlib
from pythermalcomfort.models import adaptive_en, adaptive_ashrae
from pythermalcomfort.psychrometrics import t_o

matplotlib.use("Agg")

import plotly.graph_objects as go
from dash import dcc


def chart_selector(selected_model: str, function_selection: str, chart_selected: str):

    list_charts = list(Models[selected_model].value.charts)
    if function_selection == Functionalities.Compare.value:
        if selected_model == Models.PMV_ashrae.name:
            list_charts = list(Models[selected_model].value.charts_compare)

    list_charts = [chart.name for chart in list_charts]

    if chart_selected is not None:
        chart_selected_output = chart_selected
    else:
        chart_selected_output = list_charts[0]

    drop_down_chart_dict = {
        "id": ElementsIDs.chart_selected.value,
        "question": TextHome.chart_selection.value,
        "options": list_charts,
        "multi": False,
        "default": chart_selected_output,
    }

    return generate_dropdown_inline(
        drop_down_chart_dict, value=drop_down_chart_dict["default"], clearable=False
    )


def get_inputs(inputs):
    tr = inputs[ElementsIDs.t_r_input.value]
    t_db = inputs[ElementsIDs.t_db_input.value]
    met = inputs[ElementsIDs.met_input.value]
    clo = inputs[ElementsIDs.clo_input.value]
    v = inputs[ElementsIDs.v_input.value]
    rh = inputs[ElementsIDs.rh_input.value]

    return met, clo, tr, t_db, v, rh


def compare_get_inputs(inputs):
    met_2 = inputs[ElementsIDs.met_input_input2.value]
    clo_2 = inputs[ElementsIDs.clo_input_input2.value]
    tr_2 = inputs[ElementsIDs.t_r_input_input2.value]
    t_db_2 = inputs[ElementsIDs.t_db_input_input2.value]
    v_2 = inputs[ElementsIDs.v_input_input2.value]
    rh_2 = inputs[ElementsIDs.rh_input_input2.value]

    return met_2, clo_2, tr_2, t_db_2, v_2, rh_2


def adaptive_chart(
    inputs: dict = None,
    model: str = "iso",
    units: str = "SI",
):
    traces = []

    if units == UnitSystem.IP.value:
        x_values = np.array([50, 92.3]) if model == "iso" else np.array([50, 92.3])
    else:
        x_values = np.array([10, 30]) if model == "iso" else np.array([10, 33.5])

    if model == "iso":
        adaptive_func = adaptive_en
    else:
        adaptive_func = adaptive_ashrae

    results_min = adaptive_func(
        tdb=inputs[ElementsIDs.t_db_input.value],
        tr=inputs[ElementsIDs.t_r_input.value],
        t_running_mean=x_values[0],
        v=inputs[ElementsIDs.v_input.value],
        units=units,
    )
    results_max = adaptive_func(
        tdb=inputs[ElementsIDs.t_db_input.value],
        tr=inputs[ElementsIDs.t_r_input.value],
        t_running_mean=x_values[1],
        v=inputs[ElementsIDs.v_input.value],
        units=units,
    )

    if model == "iso":
        categories = [
            ("cat_iii", "Category III", "rgba(168, 195, 161, 0.6)"),
            ("cat_ii", "Category II", "rgba(34, 139, 34, 0.5)"),
            ("cat_i", "Category I", "rgba(0, 100, 0, 0.5)"),
        ]
    else:
        categories = [
            ("80", "80% Acceptability", "rgba(144, 205, 239, 0.8)"),
            ("90", "90% Acceptability", "rgba(63, 105, 152, 0.8)"),
        ]

    for cat, name, color in categories:
        y_values_up = [
            results_min[f"tmp_cmf_{cat}_up"],
            results_max[f"tmp_cmf_{cat}_up"],
        ]
        y_values_low = [
            results_min[f"tmp_cmf_{cat}_low"],
            results_max[f"tmp_cmf_{cat}_low"],
        ]

        traces.append(
            go.Scatter(
                x=np.concatenate([x_values, x_values[::-1]]),
                y=np.concatenate([y_values_up, y_values_low[::-1]]),
                fill="toself",
                fillcolor=color,
                line=dict(color="rgba(0,0,0,0)", shape="linear"),
                name=name,
                mode="lines",
            )
        )

    x = inputs[ElementsIDs.t_rm_input.value]
    y = t_o(
        tdb=inputs[ElementsIDs.t_db_input.value],
        tr=inputs[ElementsIDs.t_r_input.value],
        v=inputs[ElementsIDs.v_input.value],
    )
    red_point = [x, y]
    traces.append(
        go.Scatter(
            x=[red_point[0]],
            y=[red_point[1]],
            mode="markers",
            marker=dict(
                color="red",
                size=6,
            ),
            name="current input",
            showlegend=False,
        )
    )

    layout = go.Layout(
        xaxis=dict(
            title=(
                "Outdoor Running Mean Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Prevailing Mean Outdoor Temperature [°F]"
            ),
            range=[10, 30] if model == "iso" else [10, 33.5],
            dtick=2 if units == UnitSystem.SI.value else 5,
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="gray",
        ),
        yaxis=dict(
            title=(
                "Operative Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Operative Temperature [°F]"
            ),
            range=[14, 36] if units == UnitSystem.SI.value else [60, 104],
            dtick=2 if units == UnitSystem.SI.value else 5,
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="gray",
        ),
        legend=dict(x=0.8, y=1),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=10, t=10),
        height=500,
        width=680,
    )

    fig = go.Figure(data=traces, layout=layout)

    if units == UnitSystem.IP.value:
        fig.update_layout(
            xaxis=dict(
                range=(
                    [50, 92.3]
                    if model == "iso"
                    else [
                        UnitConverter.celsius_to_fahrenheit(10),
                        UnitConverter.celsius_to_fahrenheit(33.5),
                    ]
                ),
            ),
        )

    return fig


def t_rh_pmv(
    inputs: dict = None,
    model: str = "iso",
    function_selection: str = Functionalities.Default,
    units: str = "SI",
):
    results = []
    pmv_limits = [-0.5, 0.5]

    met, clo, tr, t_db, v, rh = get_inputs(inputs)
    clo_d = clo_dynamic(clo, met)
    vr = v_relative(v, met)

    def calculate_pmv_results(tr, vr, met, clo):
        results = []
        for pmv_limit in pmv_limits:
            for rh in np.arange(0, 110, 10):

                def function(x):
                    return (
                        pmv(
                            x,
                            tr=tr,
                            vr=vr,
                            rh=rh,
                            met=met,
                            clo=clo,
                            wme=0,
                            standard=model,
                            units=units,
                            limit_inputs=False,
                        )
                        - pmv_limit
                    )

                temp = optimize.brentq(function, 10, 120)
                results.append(
                    {
                        "rh": rh,
                        "temp": temp,
                        "pmv_limit": pmv_limit,
                    }
                )
        return pd.DataFrame(results)

    df = calculate_pmv_results(
        tr=tr,
        vr=vr,
        met=met,
        clo=clo_d,
    )

    # Create the Plotly figure
    fig = go.Figure()

    # Add the filled area between PMV limits
    t1 = df[df["pmv_limit"] == pmv_limits[0]]
    t2 = df[df["pmv_limit"] == pmv_limits[1]]
    fig.add_trace(
        go.Scatter(
            x=t1["temp"],
            y=t1["rh"],
            fill=None,
            mode="lines",
            line=dict(color="rgba(59, 189, 237, 0.7)"),
            name=f"{model} Lower Limit",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=t2["temp"],
            y=t2["rh"],
            fill="tonexty",
            mode="lines",
            fillcolor="rgba(59, 189, 237, 0.7)",
            line=dict(color="rgba(59, 189, 237, 0.7)"),
            name=f"{model} Upper Limit",
        )
    )

    # Add scatter point for the current input
    fig.add_trace(
        go.Scatter(
            x=[t_db],
            y=[rh],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Current Input",
        )
    )

    if function_selection == Functionalities.Compare.value:
        met_2, clo_2, tr_2, t_db_2, v_2, rh_2 = compare_get_inputs(inputs)
        clo_d_compare = clo_dynamic(clo_2, met_2)
        vr_compare = v_relative(v_2, met_2)

        df_compare = calculate_pmv_results(
            tr_2,
            vr_compare,
            met_2,
            clo_d_compare,
        )
        t1_compare = df_compare[df_compare["pmv_limit"] == pmv_limits[0]]
        t2_compare = df_compare[df_compare["pmv_limit"] == pmv_limits[1]]
        fig.add_trace(
            go.Scatter(
                x=t1_compare["temp"],
                y=t1_compare["rh"],
                fill=None,
                mode="lines",
                line=dict(color="rgba(30,70,100,0.5)"),
                name=f"{model} Compare Lower Limit",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=t2_compare["temp"],
                y=t2_compare["rh"],
                fill="tonexty",
                mode="lines",
                fillcolor="rgba(30,70,100,0.5)",
                line=dict(color="rgba(30,70,100,0.5)"),
                name=f"{model} Compare Upper Limit",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[t_db_2],
                y=[rh_2],
                mode="markers",
                marker=dict(color="blue", size=8),
                name="Compare Input",
            )
        )

    # Update layout
    fig.update_layout(
        yaxis=dict(title="Relative Humidity [%]", range=[0, 100], dtick=10),
        xaxis=dict(title="Dry-bulb Temperature (°C)", range=[10, 36], dtick=2),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=10, t=0),
        height=500,
        width=680,
    )

    if units == UnitSystem.IP.value:
        fig.update_layout(
            xaxis=dict(title="Dry-bulb Temperature [°F]", range=[50, 100], dtick=5),
        )

    # Add grid lines and make the spines invisible
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")

    return fig


# Thermal heat losses vs. air temperature of ASHRAE
def get_heat_losses(inputs: dict = None, model: str = "ashrae", units: str = "SI"):
    def pmv_pdd_6_heat_loss(ta, tr, vel, rh, met, clo, wme=0):
        pa = rh * 10 * np.exp(16.6536 - 4030.183 / (ta + 235))
        icl = 0.155 * clo
        m = met * 58.15
        w = wme * 58.15
        mw = m - w

        if icl <= 0.078:
            fcl = 1 + 1.29 * icl
        else:
            fcl = 1.05 + 0.645 * icl

        hcf = 12.1 * np.sqrt(vel)
        hc = hcf
        taa = ta + 273
        tra = tr + 273
        t_cla = taa + (35.5 - ta) / (3.5 * icl + 0.1)

        p1 = icl * fcl
        p2 = p1 * 3.96
        p3 = p1 * 100
        p4 = p1 * taa
        p5 = 308.7 - 0.028 * mw + (p2 * (tra / 100.0) ** 4)
        xn = t_cla / 100
        xf = t_cla / 50
        eps = 0.00015

        n = 0
        while np.abs(xn - xf) > eps:
            xf = (xf + xn) / 2
            hcn = 2.38 * np.abs(100.0 * xf - taa) ** 0.25
            if hcf > hcn:
                hc = hcf
            else:
                hc = hcn
            xn = (p5 + p4 * hc - p2 * xf**4) / (100 + p3 * hc)
            n += 1
            if n > 150:
                raise ValueError("Max iterations exceeded")

        tcl = 100 * xn - 273

        hl1 = 3.05 * 0.001 * (5733 - 6.99 * mw - pa)
        hl2 = 0.42 * (mw - 58.15) if mw > 58.15 else 0
        hl3 = 1.7 * 0.00001 * m * (5867 - pa)
        hl4 = 0.0014 * m * (34 - ta)
        hl5 = 3.96 * fcl * (xn**4 - (tra / 100.0) ** 4)
        hl6 = fcl * hc * (tcl - ta)

        ts = 0.303 * math.exp(-0.036 * m) + 0.028
        pmv = ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6)

        ppd = 100.0 - 95.0 * math.exp(
            -0.03353 * math.pow(pmv, 4.0) - 0.2179 * math.pow(pmv, 2.0)
        )

        return {
            "pmv": pmv,
            "ppd": ppd,
            "hl1": hl1,
            "hl2": hl2,
            "hl3": hl3,
            "hl4": hl4,
            "hl5": hl5,
            "hl6": hl6,
        }

    tr = inputs[ElementsIDs.t_r_input.value]
    met = inputs[ElementsIDs.met_input.value]
    vel = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    rh = inputs[ElementsIDs.rh_input.value]
    results = {
        "h1": [],  # Water vapor diffusion through the skin
        "h2": [],  # Evaporation of sweat
        "h3": [],  # Respiration latent
        "h4": [],  # Respiration sensible
        "h5": [],  # Radiation from clothing surface
        "h6": [],  # Convection from clothing surface
        "h7": [],  # Total latent heat loss
        "h8": [],  # Total sensible heat loss
        "h9": [],  # Total heat loss
        "h10": [],  # Metabolic rate
    }

    if units == UnitSystem.IP.value:
        ta_range = np.arange(50, 105)
        for ta in ta_range:
            ta_si = UnitConverter.fahrenheit_to_celsius(ta)
            tr_si = UnitConverter.fahrenheit_to_celsius(tr)
            vel_si = UnitConverter.fps_to_mps(vel)
            heat_losses = pmv_pdd_6_heat_loss(
                ta=ta_si, tr=tr_si, vel=vel_si, rh=rh, met=met, clo=clo_d, wme=0
            )
            results["h1"].append(round(heat_losses["hl1"], 1))
            results["h2"].append(round(heat_losses["hl2"], 1))
            results["h3"].append(round(heat_losses["hl3"], 1))
            results["h4"].append(round(heat_losses["hl4"], 1))
            results["h5"].append(round(heat_losses["hl5"], 1))
            results["h6"].append(round(heat_losses["hl6"], 1))
            results["h7"].append(
                round(heat_losses["hl1"] + heat_losses["hl2"] + heat_losses["hl3"], 1)
            )
            results["h8"].append(
                round(heat_losses["hl4"] + heat_losses["hl5"] + heat_losses["hl6"], 1)
            )
            results["h9"].append(
                round(
                    heat_losses["hl1"]
                    + heat_losses["hl2"]
                    + heat_losses["hl3"]
                    + heat_losses["hl4"]
                    + heat_losses["hl5"]
                    + heat_losses["hl6"],
                    1,
                )
            )
            results["h10"].append(round(met * 58.15, 1))
    else:
        ta_range = np.arange(10, 41)
        for ta in ta_range:
            heat_losses = pmv_pdd_6_heat_loss(
                ta=ta, tr=tr, vel=vel, rh=rh, met=met, clo=clo_d, wme=0
            )
            results["h1"].append(round(heat_losses["hl1"], 1))
            results["h2"].append(round(heat_losses["hl2"], 1))
            results["h3"].append(round(heat_losses["hl3"], 1))
            results["h4"].append(round(heat_losses["hl4"], 1))
            results["h5"].append(round(heat_losses["hl5"], 1))
            results["h6"].append(round(heat_losses["hl6"], 1))
            results["h7"].append(
                round(heat_losses["hl1"] + heat_losses["hl2"] + heat_losses["hl3"], 1)
            )
            results["h8"].append(
                round(heat_losses["hl4"] + heat_losses["hl5"] + heat_losses["hl6"], 1)
            )
            results["h9"].append(
                round(
                    heat_losses["hl1"]
                    + heat_losses["hl2"]
                    + heat_losses["hl3"]
                    + heat_losses["hl4"]
                    + heat_losses["hl5"]
                    + heat_losses["hl6"],
                    1,
                )
            )
            results["h10"].append(round(met * 58.15, 1))

    fig = go.Figure()

    trace_configs = [
        ("h1", "Water vapor diffusion through the skin", "darkgreen", "legendonly"),
        ("h2", "Evaporation of sweat", "lightgreen", "legendonly"),
        ("h3", "Respiration latent", "green", "legendonly"),
        ("h4", "Respiration sensible", "darkred", "legendonly"),
        ("h5", "Radiation from clothing surface", "darkorange", "legendonly"),
        ("h6", "Convection from clothing surface", "orange", "legendonly"),
        ("h7", "Total latent ", "grey", True),
        ("h8", "Total sensible ", "lightgrey", True),
        ("h9", "Total heat loss", "black", True),
        ("h10", "Metabolic rate", "purple", True),
    ]

    for key, name, color, visible in trace_configs:
        fig.add_trace(
            go.Scatter(
                x=ta_range,
                y=results[key],
                mode="lines",
                name=name,
                visible=visible,
                line=dict(color=color),
            )
        )

    fig.update_layout(
        # title="Temperature and Heat Loss",
        xaxis=dict(
            title=(
                "Dry-bulb Air Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Dry-bulb Air Temperature [°F]"
            ),
            showgrid=True,
            showline=True,
            mirror=True,
            range=[10, 40] if units == UnitSystem.SI.value else [50, 104],
            dtick=2 if units == UnitSystem.SI.value else 5.4,
        ),
        yaxis=dict(
            title="Heat Loss [W/m²]",
            showgrid=True,
            showline=True,
            mirror=True,
            range=[-40, 120],
            dtick=20,
        ),
        legend=dict(
            x=0.5,
            y=-0.2,
            orientation="h",
            traceorder="normal",
            xanchor="center",
            yanchor="top",
        ),
        template="plotly_white",
        autosize=False,
        margin=dict(l=0, r=10, t=0),
        height=600,
        width=600,
    )

    return fig


# SET outputs chart of ASHRAE
def SET_outputs_chart(
    inputs: dict = None,
    calculate_ce: bool = False,
    p_atmospheric: int = 101325,
    body_position="standing",
    units: str = "SI",
):
    # create tdb list for plotting lines when tdb is x-axis
    tdb_values = np.arange(10, 41, 5, dtype=float).tolist()

    # Prepare arrays for the outputs we want to plot
    set_temp = []  # set_tmp()
    skin_temp = []  # t_skin
    core_temp = []  # t_core
    clothing_temp = []  # t_cl
    mean_body_temp = []  # t_body
    total_skin_evaporative_heat_loss = []  # e_skin
    sweat_evaporation_skin_heat_loss = []  # e_rsw
    vapour_diffusion_skin_heat_loss = []  # e_diff
    total_skin_sensible_heat_loss = []  # q_sensible
    total_skin_heat_loss = []  # q_skin
    heat_loss_respiration = []  # q_res
    skin_wettedness = []  # w

    # Extract common input values
    tr = float(inputs[ElementsIDs.t_r_input.value])
    vr = float(
        v_relative(  # Ensure vr is scalar
            v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
        )
    )
    rh = float(inputs[ElementsIDs.rh_input.value])  # Ensure rh is scalar
    met = float(inputs[ElementsIDs.met_input.value])  # Ensure met is scalar
    clo = float(
        clo_dynamic(  # Ensure clo is scalar
            clo=inputs[ElementsIDs.clo_input.value],
            met=inputs[ElementsIDs.met_input.value],
        )
    )

    if units == UnitSystem.IP.value:
        tr = round(float(units_converter(tr=tr)[0]), 1)
        vr = round(float(units_converter(vr=vr)[0]), 1)

    for tdb in tdb_values:
        ce = cooling_effect(
            tdb=tdb,
            tr=tr,
            vr=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
        )

        # Iterate through each temperature value and call `two_nodes`
        results = two_nodes(
            tdb=tdb,
            tr=tr,
            v=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
            p_atmospheric=p_atmospheric,
            body_position=body_position,
            calculate_ce=calculate_ce,
        )

        # Collect relevant data for each variable, converting to float
        set_temp.append(
            float(results["_set"]) - ce
        )  # Convert np.float64 to float & Manual Cooling effect
        skin_temp.append(
            float(results["t_skin"]) - ce
        )  # Convert np.float64 to float & Manual Cooling effect
        core_temp.append(
            float(results["t_core"]) - ce
        )  # Convert np.float64 to float & Manual Cooling effect
        total_skin_evaporative_heat_loss.append(
            float(results["e_skin"])
        )  # Convert np.float64 to float
        sweat_evaporation_skin_heat_loss.append(
            float(results["e_rsw"])
        )  # Convert np.float64 to float
        vapour_diffusion_skin_heat_loss.append(
            float(results["e_skin"] - results["e_rsw"])
        )  # Convert np.float64 to float
        total_skin_sensible_heat_loss.append(
            float(results["q_sensible"])
        )  # Convert np.float64 to float
        total_skin_heat_loss.append(
            float(results["q_skin"])
        )  # Convert np.float64 to float
        heat_loss_respiration.append(
            float(results["q_res"])
        )  # Convert np.float64 to float
        skin_wettedness.append(
            float(results["w"]) * 100
        )  # Convert to percentage and float

        # progress from two_nodes() for final clothing temperature t_cl & mean body temperature t_body
        alfa = 0.1
        sbc = 0.000000056697
        pressure_in_atmospheres = float(p_atmospheric / 101325)
        length_time_simulation = 60  # length time simulation
        n_simulation = 0
        r_clo = 0.155 * clo
        f_a_cl = 1.0 + 0.15 * clo
        h_cc = 3.0 * pow(pressure_in_atmospheres, 0.53)
        h_fc = 8.600001 * pow((vr * pressure_in_atmospheres), 0.53)
        h_cc = max(h_cc, h_fc)
        if not calculate_ce and met > 0.85:
            h_c_met = 5.66 * (met - 0.85) ** 0.39
            h_cc = max(h_cc, h_c_met)
        h_r = 4.7
        h_t = h_r + h_cc
        r_a = 1.0 / (f_a_cl * h_t)
        t_op = (h_r * tr + h_cc * tdb) / h_t

        while n_simulation < length_time_simulation:

            n_simulation += 1

            iteration_limit = 150  # for following while loop
            # t_cl temperature of the outer surface of clothing
            t_cl = (r_a * results["t_skin"] + r_clo * t_op) / (
                r_a + r_clo
            )  # initial guess
            n_iterations = 0
            tc_converged = False
            while not tc_converged:
                # update h_r
                # 0.95 is the clothing emissivity from ASHRAE fundamentals Ch. 9.7 Eq. 35
                if body_position == "sitting":
                    # 0.7 ratio between radiation area of the body and the body area
                    h_r = 4.0 * 0.95 * sbc * ((t_cl + tr) / 2.0 + 273.15) ** 3.0 * 0.7
                else:  # if standing
                    # 0.73 ratio between radiation area of the body and the body area
                    h_r = 4.0 * 0.95 * sbc * ((t_cl + tr) / 2.0 + 273.15) ** 3.0 * 0.73
                h_t = h_r + h_cc
                r_a = 1.0 / (f_a_cl * h_t)
                t_op = (h_r * tr + h_cc * tdb) / h_t
                t_cl_new = (r_a * results["t_skin"] + r_clo * t_op) / (r_a + r_clo)
                if abs(t_cl_new - t_cl) <= 0.01:
                    tc_converged = True
                t_cl = t_cl_new
                n_iterations += 1

                if n_iterations > iteration_limit:
                    raise StopIteration("Max iterations exceeded")

            t_body = alfa * results["t_skin"] + (1 - alfa) * results["t_core"]
            # update alfa
            alfa = 0.0417737 + 0.7451833 / (results["m_bl"] + 0.585417)
        # get final clothing temperature t_cl
        clothing_temp.append(
            float(t_cl) - ce
        )  # Convert np.float64 to float & Manual Cooling effect
        # get final mean body temperature t_body
        mean_body_temp.append(
            float(t_body) - ce
        )  # Convert np.float64 to float & Manual Cooling effect

    if units == UnitSystem.IP.value:
        tdb_values = list(
            map(
                lambda x: round(float(units_converter(tdb=x, from_units="si")[0]), 1),
                tdb_values,
            )
        )
        set_temp = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                set_temp,
            )
        )
        skin_temp = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                skin_temp,
            )
        )
        core_temp = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                core_temp,
            )
        )
        clothing_temp = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                clothing_temp,
            )
        )
        mean_body_temp = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                mean_body_temp,
            )
        )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=set_temp,
            mode="lines",
            name="SET temperature",
            line=dict(color="blue"),
            yaxis="y1",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=skin_temp,
            mode="lines",
            name="Skin temperature",
            line=dict(color="cyan"),
        )
    )

    # core temperature curve
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=core_temp,
            mode="lines",
            name="Core temperature",
            line=dict(color="limegreen"),
            yaxis="y1",  # Use a second y-axis
        )
    )

    # Clothing temperature
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=clothing_temp,
            mode="lines",
            name="Clothing temperature",
            line=dict(color="lightgreen"),
            yaxis="y1",  # Use a second y-axis
        )
    )

    # Mean body temperature
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=mean_body_temp,
            mode="lines",
            name="Mean body temperature",
            visible="legendonly",
            line=dict(color="green"),
            yaxis="y1",  # Use a second y-axis
        )
    )

    # total skin evaporative heat loss
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=total_skin_evaporative_heat_loss,
            mode="lines",
            name="Total skin evaporative heat loss",
            visible="legendonly",
            line=dict(color="lightgrey"),
            yaxis="y2",  # Use a second y-axis
        )
    )
    # sweat evaporation skin heat loss
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=sweat_evaporation_skin_heat_loss,
            mode="lines",
            name="Sweat evaporation skin heat loss ",
            visible="legendonly",
            line=dict(color="orange"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    # vapour diffusion skin heat loss
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=vapour_diffusion_skin_heat_loss,
            mode="lines",
            name="Vapour diffusion skin heat loss ",
            visible="legendonly",
            line=dict(color="darkorange"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    # total skin sensible heat loss
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=total_skin_heat_loss,
            mode="lines",
            name="Total skin sensible heat loss ",
            visible="legendonly",
            line=dict(color="darkgrey"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    # total skin heat loss curve
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=total_skin_heat_loss,
            mode="lines",
            name="Total skin heat loss",
            line=dict(color="black"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    #  heat loss respiration curve
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=heat_loss_respiration,
            mode="lines",
            name="Heat loss respiration",
            line=dict(color="black", dash="dash"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    #  skin moisture curve
    fig.add_trace(
        go.Scatter(
            x=tdb_values,
            y=skin_wettedness,
            mode="lines",
            name="Skin wettedness",
            visible="legendonly",
            line=dict(color="yellow"),
            yaxis="y2",  # Use a second y-axis
        )
    )

    #  layout of the chart and adjust the legend position
    fig.update_layout(
        xaxis=dict(
            title=(
                "Dry-bulb Air Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Dry-bulb Temperature [°F]"
            ),
            showgrid=False,
            range=[10, 40] if units == UnitSystem.SI.value else [50, 104],
            dtick=2 if units == UnitSystem.SI.value else 5.4,
        ),
        yaxis=dict(
            title=(
                "Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Temperature [°F]"
            ),
            showgrid=False,
            range=[18, 38] if units == UnitSystem.SI.value else [60, 100],
            dtick=2 if units == UnitSystem.SI.value else 5,
        ),
        yaxis2=dict(
            title="Heat Loss [W] / Skin Wettedness [%]",
            showgrid=False,
            overlaying="y",
            side="right",
            range=[0, 70],
        ),
        legend=dict(
            x=0.5,
            y=-0.2,
            orientation="h",
            traceorder="normal",
            xanchor="center",
            yanchor="top",
        ),
        template="plotly_white",
        autosize=False,
        margin=dict(l=0, r=10, t=0),
        height=600,
        width=600,
    )
    return fig
