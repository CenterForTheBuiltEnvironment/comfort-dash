import base64
import io
from copy import deepcopy

import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pythermalcomfort.models import pmv
from pythermalcomfort.utilities import v_relative, clo_dynamic
from scipy import optimize

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, Models, Functionalities
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


# # fig example
# def t_rh_pmv(inputs: dict = None, model: str = "iso", function_selection: str = Functionalities):
#     results = []
#     pmv_limits = [-0.5, 0.5]
#     clo_d = clo_dynamic(
#         clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
#     )
#     vr = v_relative(
#         v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
#     )
#     for pmv_limit in pmv_limits:
#         for rh in np.arange(0, 110, 10):

#             def function(x):
#                 return (
#                     pmv(
#                         x,
#                         tr=inputs[ElementsIDs.t_r_input.value],
#                         vr=vr,
#                         rh=rh,
#                         met=inputs[ElementsIDs.met_input.value],
#                         clo=clo_d,
#                         wme=0,
#                         standard=model,
#                         limit_inputs=False,
#                     )
#                     - pmv_limit
#                 )

#             temp = optimize.brentq(function, 10, 40)
#             results.append(
#                 {
#                     "rh": rh,
#                     "temp": temp,
#                     "pmv_limit": pmv_limit,
#                 }
#             )

#     df = pd.DataFrame(results)

#     f, axs = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
#     t1 = df[df["pmv_limit"] == pmv_limits[0]]
#     t2 = df[df["pmv_limit"] == pmv_limits[1]]
#     axs.fill_betweenx(
#         t1["rh"], t1["temp"], t2["temp"], alpha=0.5, label=model, color="#7BD0F2"
#     )
#     axs.scatter(
#         inputs[ElementsIDs.t_db_input.value],
#         inputs[ElementsIDs.rh_input.value],
#         color="red",
#     )
#     axs.set(
#         ylabel="RH (%)",
#         xlabel="Temperature (°C)",
#         ylim=(0, 100),
#         xlim=(10, 40),
#     )
#     axs.legend(frameon=False).remove()
#     axs.grid(True, which="both", linestyle="--", linewidth=0.5)
#     axs.spines["top"].set_visible(False)
#     axs.spines["right"].set_visible(False)
#     plt.tight_layout()

#     my_stringIObytes = io.BytesIO()
#     plt.savefig(
#         my_stringIObytes,
#         format="png",
#         transparent=True,
#         dpi=300,
#         bbox_inches="tight",
#         pad_inches=0,
#     )
#     my_stringIObytes.seek(0)
#     my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
#     plt.close("all")
#     return dmc.Image(
#         src=f"data:image/png;base64, {my_base64_jpgData}",
#         alt="Heat stress chart",
#         py=0,
#     )


def t_rh_pmv(
    inputs: dict = None,
    model: str = "iso",
    function_selection: str = Functionalities.Default,
):
    results = []
    pmv_limits = [-0.5, 0.5]

    # Extract the values for the first set of inputs
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )

    # # Print keys to debug
    # print("Available keys in inputs:", inputs.keys())

    # Initialize comparison values if in Compare mode
    if function_selection == Functionalities.Compare.value:
        try:
            clo_d_compare = clo_dynamic(
                clo=inputs.get(ElementsIDs.clo_input_input2.value),
                met=inputs.get(ElementsIDs.met_input_input2.value),
            )
            vr_compare = v_relative(
                v=inputs.get(ElementsIDs.v_input_input2.value),
                met=inputs.get(ElementsIDs.met_input_input2.value),
            )
        except KeyError as e:
            print(f"KeyError: {e}. Skipping comparison plotting.")
            clo_d_compare, vr_compare = None, None

    # Helper function to calculate PMV results
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
        return pd.DataFrame(results)

    # Calculate results for the first set of inputs
    df = calculate_pmv_results(
        tr=inputs[ElementsIDs.t_r_input.value],
        vr=vr,
        met=inputs[ElementsIDs.met_input.value],
        clo=clo_d,
    )

    # Create the plot
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

    # If in Compare mode and the comparison values exist, plot the second set of inputs
    if (
        function_selection == Functionalities.Compare.value
        and clo_d_compare is not None
    ):
        df_compare = calculate_pmv_results(
            tr=inputs[ElementsIDs.t_r_input_input2.value],
            vr=vr_compare,
            met=inputs[ElementsIDs.met_input_input2.value],
            clo=clo_d_compare,
        )
        t1_compare = df_compare[df_compare["pmv_limit"] == pmv_limits[0]]
        t2_compare = df_compare[df_compare["pmv_limit"] == pmv_limits[1]]
        axs.fill_betweenx(
            t1_compare["rh"],
            t1_compare["temp"],
            t2_compare["temp"],
            alpha=0.3,
            label=model + " Compare",
            color="#808080",
        )
        axs.scatter(
            inputs[ElementsIDs.t_db_input_input2.value],
            inputs[ElementsIDs.rh_input_input2.value],
            color="blue",
        )

    # Set axis labels, limits, and other plot settings
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

    # Convert plot to base64 string
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
