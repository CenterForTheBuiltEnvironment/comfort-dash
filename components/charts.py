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

import plotly.graph_objects as go
from dash import dcc


def chart_selector(selected_model: str, function_selection: str):

    list_charts = deepcopy(Models[selected_model].value.charts)
    if function_selection == Functionalities.Compare.value:
        if selected_model == Models.PMV_ashrae.name:
            list_charts = deepcopy(Models[selected_model].value.charts_compare)

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


def t_rh_pmv(
    inputs: dict = None,
    model: str = "iso",
    function_selection: str = Functionalities.Default,
):
    results = []
    pmv_limits = [-0.5, 0.5]
    # todo determine if the value is IP unit , transfer to SI
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )

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

                temp = optimize.brentq(function, 10, 100)
                results.append(
                    {
                        "rh": rh,
                        "temp": temp,
                        "pmv_limit": pmv_limit,
                    }
                )
        return pd.DataFrame(results)

    df = calculate_pmv_results(
        tr=inputs[ElementsIDs.t_r_input.value],
        vr=vr,
        met=inputs[ElementsIDs.met_input.value],
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
            x=[inputs[ElementsIDs.t_db_input.value]],
            y=[inputs[ElementsIDs.rh_input.value]],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Current Input",
        )
    )

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
                x=[inputs[ElementsIDs.t_db_input_input2.value]],
                y=[inputs[ElementsIDs.rh_input_input2.value]],
                mode="markers",
                marker=dict(color="blue", size=8),
                name="Compare Input",
            )
        )

    # todo add mouse x,y axis parameter to here

    annotation_text = (
        f"t<sub>db</sub>   {inputs[ElementsIDs.t_db_input.value]:.1f} °C<br>"
    )

    fig.add_annotation(
        x=32,
        y=96,
        xref="x",
        yref="y",
        text=annotation_text,
        showarrow=False,
        align="left",
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=14),
    )

    # Update layout
    fig.update_layout(
        yaxis=dict(title="RH (%)", range=[0, 100], dtick=10),
        xaxis=dict(title="Temperature (°C)", range=[10, 40], dtick=2),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # Add grid lines and make the spines invisible
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")

    return fig
