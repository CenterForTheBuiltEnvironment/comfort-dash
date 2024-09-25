import base64
import io
import math
from copy import deepcopy

import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pythermalcomfort import set_tmp, two_nodes
from pythermalcomfort.models import pmv, adaptive_ashrae
from pythermalcomfort.utilities import v_relative, clo_dynamic
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
from pythermalcomfort.models import adaptive_en
from pythermalcomfort.psychrometrics import t_o

matplotlib.use("Agg")

import plotly.graph_objects as go
from dash import dcc


def chart_selector(selected_model: str, function_selection: str):
    list_charts = list(Models[selected_model].value.charts)
    if function_selection == Functionalities.Compare.value:
        if selected_model == Models.PMV_ashrae.name:
            list_charts = list(Models[selected_model].value.charts_compare)

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


def adaptive_chart(inputs: dict = None,
                   model: str = "iso",
                   units: str = "SI", ):
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
            ("cat_iii", "Category III", "rgba(144, 238, 144, 0.3)"),
            ("cat_ii", "Category II", "rgba(34, 139, 34, 0.5)"),
            ("cat_i", "Category I", "rgba(0, 100, 0, 0.7)"),
        ]
    else:
        categories = [
            ("80", "80% Acceptability", "rgba(0, 100, 200, 0.2)"),
            ("90", "90% Acceptability", "rgba(0, 100, 200, 0.4)"),
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
            title="Outdoor Running Mean Temperature [°C]" if units == UnitSystem.SI.value else "Prevailing Mean Outdoor Temperature [°F]",
            range=[10, 30] if model == "iso" else [10, 33.5],
            dtick=2 if units == UnitSystem.SI.value else 5,
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1.5,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="black",
        ),
        yaxis=dict(
            title="Operative Temperature [°C]" if units == UnitSystem.SI.value else "Operative Temperature [°F]",
            range=[14, 36] if units == UnitSystem.SI.value else [60, 104],
            dtick=2 if units == UnitSystem.SI.value else 5,
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1.5,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="black",
        ),
        legend=dict(x=0.8, y=1),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig = go.Figure(data=traces, layout=layout)

    if units == UnitSystem.IP.value:
        fig.update_layout(
            xaxis=dict(
                range=[50, 92.3] if model == "iso" else [UnitConverter.celsius_to_fahrenheit(10),
                                                         UnitConverter.celsius_to_fahrenheit(33.5)],
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
    if model == "iso":
        pmv_limits = [-0.7, -0.5, -0.2, 0.2, 0.5, 0.7]
        colors = [
            "rgba(168,204,162,0.9)",
            "rgba(114,174,106,0.9)",
            "rgba(78,156,71,0.9)",
            "rgba(114,174,106,0.9)",
            "rgba(168,204,162,0.9)",
        ]
    else:  # ASHRAE
        pmv_limits = [-0.5, 0.5]
        colors = ["rgba(59, 189, 237, 0.7)"]

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

                try:
                    temp = optimize.brentq(function, 10, 120)
                    results.append(
                        {
                            "rh": rh,
                            "temp": temp,
                            "pmv_limit": pmv_limit,
                        }
                    )
                except ValueError:
                    continue
        return pd.DataFrame(results)

    df = calculate_pmv_results(
        tr=tr,
        vr=vr,
        met=met,
        clo=clo_d,
    )

    fig = go.Figure()

    for i in range(len(pmv_limits) - 1):
        t1 = df[df["pmv_limit"] == pmv_limits[i]]
        t2 = df[df["pmv_limit"] == pmv_limits[i + 1]]
        fig.add_trace(
            go.Scatter(
                x=t1["temp"],
                y=t1["rh"],
                fill=None,
                mode="lines",
                line=dict(color=colors[i]),
                name=f"{model} Lower Limit",
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=t2["temp"],
                y=t2["rh"],
                fill="tonexty",
                mode="lines",
                fillcolor=colors[i],
                line=dict(color=colors[i]),
                name=f"{model} Upper Limit",
                hoverinfo="skip",
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
            # hoverinfo="skip",
        )
    )

    if model == "ashrae" and function_selection == Functionalities.Compare.value:
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
                hoverinfo='skip'
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
                hoverinfo='skip'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[t_db_2],
                y=[rh_2],
                mode="markers",
                marker=dict(color="blue", size=8),
                name="Compare Input",
                hoverinfo='skip'
            )
        )

    fig.update_layout(
        yaxis=dict(title="Relative Humidity [%]", range=[0, 100], dtick=10),
        xaxis=dict(title="Dry-bulb Temperature (°C)", range=[10, 36], dtick=2),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
    )

    if units == UnitSystem.IP.value:
        fig.update_layout(
            xaxis=dict(title="Dry-bulb Temperature [°F]", range=[50, 100], dtick=5),
        )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")

    return fig


def SET_outputs_chart(
    inputs: dict = None, calculate_ce: bool = False, p_atmospheric: int = 101325
):
    # Dry-bulb air temperature (x-axis)
    tdb_values = np.arange(10, 40, 0.5, dtype=float).tolist()

    # Prepare arrays for the outputs we want to plot
    set_temp = []  # set_tmp()
    skin_temp = []  # t_skin
    core_temp = []  # t_core
    clothing_temp = []  # t_cl
    mean_body_temp = []  # t_body
    total_skin_evaporative_heat_loss = []  # e_skin
    sweat_evaporation_skin_heat_loss = []  # e_rsw
    vapour_diffusion_skin_heat_loss = []  # e_diff
    total_skin_senesible_heat_loss = []  # q_sensible
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
            clo=inputs[ElementsIDs.clo_input.value], met=met
        )
    )

    # Iterate through each temperature value and call set_tmp
    for tdb in tdb_values:
        set = set_tmp(
            tdb=tdb,
            tr=tr,
            v=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
            limit_inputs=False,
        )
        set_temp.append(float(set))  # Convert np.float64 to float

    # Iterate through each temperature value and call `two_nodes`
    for tdb in tdb_values:
        results = two_nodes(
            tdb=tdb,
            tr=tr,
            v=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
        )
        # Collect relevant data for each variable, converting to float
        skin_temp.append(float(results["t_skin"]))  # Convert np.float64 to float
        core_temp.append(float(results["t_core"]))  # Convert np.float64 to float
        total_skin_evaporative_heat_loss.append(
            float(results["e_skin"])
        )  # Convert np.float64 to float
        sweat_evaporation_skin_heat_loss.append(
            float(results["e_rsw"])
        )  # Convert np.float64 to float
        vapour_diffusion_skin_heat_loss.append(
            float(results["e_skin"] - results["e_rsw"])
        )  # Convert np.float64 to float
        total_skin_senesible_heat_loss.append(
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

        # calculate clothing temperature t_cl
        pressure_in_atmospheres = float(p_atmospheric / 101325)
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
        clothing_temp.append(
            float((r_a * results["t_skin"] + r_clo * t_op) / (r_a + r_clo))
        )
        # calculate mean body temperature t_body
        alfa = 0.1
        mean_body_temp.append(
            float(alfa * results["t_skin"] + (1 - alfa) * results["t_core"])
        )
    # df = pd.DataFrame(results)
    fig = go.Figure()
    # fig.add_trace(go.Scatter(
    #     x=tdb_values,
    #     y=set_temp,
    #     mode='lines',
    #     name='SET temperature',
    #     line=dict(color='blue')
    # ))

    # Added SET temperature curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=set_temp,
        mode='lines',
        name='SET temperature',
        line=dict(color='blue'),
        yaxis='y1'  # Use a  y-axis
    ))


    # Adding skin temperature curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=skin_temp,
        mode='lines',
        name='Skin temperature',
        line=dict(color='cyan')
    ))

    # Added core temperature curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=core_temp,
        mode='lines',
        name='Core temperature',
        line=dict(color='limegreen'),
        yaxis='y1'  # Use a second y-axis
    ))

    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=clothing_temp,
        mode='lines',
        name='Clothing temperature',
        line=dict(color='lightgreen'),
        yaxis='y1'  # Use a second y-axis
    ))

    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=mean_body_temp,
        mode='lines',
        name='Mean body temperature',
        visible='legendonly',
        line=dict(color='green'),
        yaxis='y1'  # Use a second y-axis
    ))
#total skin evaporative heat loss
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=total_skin_evaporative_heat_loss,
        mode='lines',
        name='Total skin evaporative heat loss',
        visible='legendonly',
        line=dict(color='lightgrey'),
        yaxis='y2'  # Use a second y-axis
    ))
# sweat evaporation skin heat loss
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=sweat_evaporation_skin_heat_loss,
        mode='lines',
        name='Sweat evaporation skin heat loss ',
        visible='legendonly',
        line=dict(color='orange'),
        yaxis='y2'  # Use a second y-axis
    ))

    # vapour diffusion skin heat loss
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=vapour_diffusion_skin_heat_loss,
        mode='lines',
        name='Vapour diffusion skin heat loss ',
        visible='legendonly',
        line=dict(color='darkorange'),
        yaxis='y2'  # Use a second y-axis
    ))

    # total skin sensible heat loss
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=total_skin_heat_loss,
        mode='lines',
        name='Total skin sensible heat loss ',
        visible='legendonly',
        line=dict(color='darkgrey'),
        yaxis='y2'  # Use a second y-axis
    ))


    # Added  total skin heat loss curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=total_skin_heat_loss,
        mode='lines',
        name='Total skin heat loss',
        line=dict(color='black'),
        yaxis='y2'  # Use a second y-axis
    ))

    #  heat loss respiration curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=heat_loss_respiration,
        mode='lines',
        name='Heat loss respiration',
        line=dict(color='black', dash='dash'),
        yaxis='y2'  # Use a second y-axis
    ))


    # Added skin moisture curve
    fig.add_trace(go.Scatter(
        x=tdb_values,
        y=skin_wettedness,
        mode='lines',
        name='Skin wettedness',
        visible='legendonly',
        line=dict(color='yellow'),
        yaxis='y2'  # Use a second y-axis
    ))






    # Set the layout of the chart and adjust the legend position
    fig.update_layout(
        # title='Temperature and Heat Loss',
        xaxis=dict(title='Dry-bulb Air Temperature [°C]', showgrid = False, range=[10, 40],dtick=2 ),
        yaxis=dict(title='Temperature [°C]', showgrid = False, range=[18, 38],dtick=2 ),
        yaxis2=dict(
            title='Heat Loss [W] / Skin Wettedness [%]',
            showgrid=False,
            overlaying='y',
            side='right',
            range=[0, 70],
            # title_standoff=50  # Increase the distance between the Y axis title and the chart
        ),
        legend=dict(
            x=0.5,  # Adjust the horizontal position of the legend
            y=-0.2,  # Move the legend below the chart
            orientation='h',  # Display the legend horizontally
            traceorder="normal",
            xanchor='center',
            yanchor='top',


        ),
        template='plotly_white',
        autosize=False,
        width=700,  # 3:4
        height=700  # 3:4
    )

    # show
    return fig


def speed_temp_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )

    for pmv_limit in pmv_limits:
        for vr in np.arange(0.1, 1.3, 0.1):

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=inputs[ElementsIDs.rh_input.value],
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
                    "vr": vr,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )
    df = pd.DataFrame(results)
    fig = go.Figure()

    # Define trace1
    fig.add_trace(
        go.Scatter(
            x=df[df["pmv_limit"] == pmv_limits[0]]["temp"],
            y=df[df["pmv_limit"] == pmv_limits[0]]["vr"],
            mode="lines",
            # fill='tozerox',
            # fillcolor='rgba(123, 208, 242, 0.5)',
            name=f"PMV {pmv_limits[0]}",
            showlegend=False,
            line=dict(color="rgba(0,0,0,0)"),
        )
    )

    # Define trace2
    fig.add_trace(
        go.Scatter(
            x=df[df["pmv_limit"] == pmv_limits[1]]["temp"],
            y=df[df["pmv_limit"] == pmv_limits[1]]["vr"],
            mode="lines",
            fill="tonextx",
            fillcolor="rgba(123, 208, 242, 0.5)",
            name=f"PMV {pmv_limits[1]}",
            showlegend=False,
            line=dict(color="rgba(0,0,0,0)"),
        )
    )

    # Define input point
    fig.add_trace(
        go.Scatter(
            x=[inputs[ElementsIDs.t_db_input.value]],
            y=[inputs[ElementsIDs.v_input.value]],
            mode="markers",
            marker=dict(color="red"),
            name="Input",
            showlegend=False,
        )
    )

    fig.update_layout(
        xaxis_title="Operative Temperature [°C]",  # x title
        yaxis_title="Relative Air Speed [m/s]",  # y title
        template="plotly_white",
        width=700,
        height=525,
        xaxis=dict(
            range=[20, 34],  # x range
            tickmode="linear",
            tick0=20,
            dtick=2,
            gridcolor="lightgrey",
        ),
        yaxis=dict(
            range=[0.0, 1.2],  # y range
            tickmode="linear",
            tick0=0.0,
            dtick=0.1,
            gridcolor="lightgrey",
        ),
    )
    # Return the figure
    return fig
def get_heat_losses(inputs: dict = None, model: str = "ashrae"):
    tr = inputs[ElementsIDs.t_r_input.value]
    met = inputs[ElementsIDs.met_input.value]
    vel = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    rh = inputs[ElementsIDs.rh_input.value]

    ta_range = np.arange(10, 41)
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
        ("h7", "Total latent heat loss", "grey", True),
        ("h8", "Total sensible heat loss", "lightgrey", True),
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
            title="Dry-bulb Air Temperature [°C]",
            showgrid=True,
            range=[10, 40],
            dtick=2,
        ),
        yaxis=dict(title="Heat Loss [W/m²]", showgrid=True, range=[10, 120], dtick=20),
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
        width=700,
        height=700,
    )

    return fig

# for calculate pmv & ppd & 6 heat loss
def pmv_pdd_6_heat_loss(ta, tr, vel, rh, met, clo, wme=0):

    pa = rh * 10 * math.exp(16.6536 - 4030.183 / (ta + 235))
    icl = 0.155 * clo
    m = met * 58.15
    w = wme * 58.15
    mw = m - w

    if icl <= 0.078:
        fcl = 1 + 1.29 * icl
    else:
        fcl = 1.05 + 0.645 * icl

    hcf = 12.1 * math.sqrt(vel)
    taa = ta + 273
    tra = tr + 273

    t_cla = taa + (35.5 - ta) / (3.5 * icl + 0.1)

    p1 = icl * fcl
    p2 = p1 * 3.96
    p3 = p1 * 100
    p4 = p1 * taa
    p5 = 308.7 - 0.028 * mw + p2 * math.pow(tra / 100, 4)
    xn = t_cla / 100
    xf = t_cla / 50
    eps = 0.00015

    n = 0
    while abs(xn - xf) > eps:
        xf = (xf + xn) / 2
        hcn = 2.38 * math.pow(abs(100.0 * xf - taa), 0.25)
        hc = hcf if hcf > hcn else hcn
        xn = (p5 + p4 * hc - p2 * math.pow(xf, 4)) / (100 + p3 * hc)
        n += 1
        if n > 150:
            raise ValueError("Max iterations exceeded")

    tcl = 100 * xn - 273

    hl1 = 3.05 * 0.001 * (5733 - 6.99 * mw - pa)
    hl2 = 0.42 * (mw - 58.15) if mw > 58.15 else 0
    hl3 = 1.7 * 0.00001 * m * (5867 - pa)
    hl4 = 0.0014 * m * (34 - ta)
    hl5 = 3.96 * fcl * (math.pow(xn, 4) - math.pow(tra / 100, 4))
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