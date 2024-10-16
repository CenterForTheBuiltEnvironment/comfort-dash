import base64
import io
from copy import deepcopy

import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pythermalcomfort.models import pmv
from pythermalcomfort.utilities import v_relative, clo_dynamic, units_converter
from scipy import optimize

from scipy.optimize import fsolve

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
from pythermalcomfort.psychrometrics import psy_ta_rh, t_o

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


def adaptive_en_chart(inputs, units):
    traces = []

    if units == UnitSystem.IP.value:
        x_values = np.array([50, 92.3])
    else:
        x_values = np.array([10, 30])

    results_min = adaptive_en(
        tdb=inputs[ElementsIDs.t_db_input.value],
        tr=inputs[ElementsIDs.t_r_input.value],
        t_running_mean=x_values[0],
        v=inputs[ElementsIDs.v_input.value],
        units=units,
    )
    results_max = adaptive_en(
        tdb=inputs[ElementsIDs.t_db_input.value],
        tr=inputs[ElementsIDs.t_r_input.value],
        t_running_mean=x_values[1],
        v=inputs[ElementsIDs.v_input.value],
        units=units,
    )

    y_values_cat_iii_up = [
        results_min["tmp_cmf_cat_iii_up"],
        results_max["tmp_cmf_cat_iii_up"],
    ]
    y_values_cat_iii_low = [
        results_min["tmp_cmf_cat_iii_low"],
        results_max["tmp_cmf_cat_iii_low"],
    ]

    y_values_cat_ii_up = [
        results_min["tmp_cmf_cat_ii_up"],
        results_max["tmp_cmf_cat_ii_up"],
    ]
    y_values_cat_ii_low = [
        results_min["tmp_cmf_cat_ii_low"],
        results_max["tmp_cmf_cat_ii_low"],
    ]

    y_values_cat_i_up = [
        results_min["tmp_cmf_cat_i_up"],
        results_max["tmp_cmf_cat_i_up"],
    ]
    y_values_cat_i_low = [
        results_min["tmp_cmf_cat_i_low"],
        results_max["tmp_cmf_cat_i_low"],
    ]

    # traces[0]
    traces.append(
        go.Scatter(
            x=np.concatenate([x_values, x_values[::-1]]),
            y=np.concatenate([y_values_cat_iii_up, y_values_cat_iii_low[::-1]]),
            fill="toself",
            fillcolor="rgba(144, 238, 144, 0.3)",
            line=dict(color="rgba(144, 238, 144, 0)", shape="linear"),
            name="Category III",
            mode="lines",
        )
    )
    # traces[1]
    traces.append(
        go.Scatter(
            x=np.concatenate([x_values, x_values[::-1]]),
            y=np.concatenate([y_values_cat_ii_up, y_values_cat_ii_low[::-1]]),
            fill="toself",
            fillcolor="rgba(34, 139, 34, 0.5)",
            line=dict(color="rgba(34, 139, 34, 0)", shape="linear"),
            name="Category II",
            mode="lines",
        )
    )
    # traces[2]
    traces.append(
        go.Scatter(
            x=np.concatenate([x_values, x_values[::-1]]),
            y=np.concatenate([y_values_cat_i_up, y_values_cat_i_low[::-1]]),
            fill="toself",
            fillcolor="rgba(0, 100, 0, 0.7)",
            line=dict(color="rgba(0, 100, 0, 0)", shape="linear"),
            name="Category I",
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
    # traces[3]
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
    # theta = np.linspace(0, 2 * np.pi, 100)
    # circle_x = red_point[0] + 0.5 * np.cos(theta)
    # circle_y = red_point[1] + 0.8 * np.sin(theta)
    # # traces[4]
    # traces.append(
    #     go.Scatter(
    #         x=circle_x,
    #         y=circle_y,
    #         mode="lines",
    #         line=dict(color="red", width=2.5),
    #         # name='circle',
    #         showlegend=False,
    #     )
    # )

    layout = go.Layout(
        xaxis=dict(
            title="Outdoor Running Mean Temperature [°C]",
            range=[10, 30],
            dtick=2,
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
            title="Operative Temperature [°C]",
            range=[14, 36],
            dtick=2,
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
                title="Outdoor Running Mean Temperature [°F]", range=[50, 92.3], dtick=5
            ),
        )
        fig.update_layout(
            yaxis=dict(title="Operative Temperature [°F]", range=[60, 104], dtick=5),
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
        margin=dict(l=40, r=40, t=40, b=40),
    )

    if units == UnitSystem.IP.value:
        fig.update_layout(
            xaxis=dict(title="Dry-bulb Temperature [°F]", range=[50, 100], dtick=5),
        )

    # Add grid lines and make the spines invisible
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")

    return fig

# function in pmv_ppd()
def _pmv_ppd_optimized(tdb, tr, vr, rh, met, clo, wme=0):
    pa = rh * 10 * np.exp(16.6536 - 4030.183 / (tdb + 235))

    icl = 0.155 * clo  # thermal insulation of the clothing in M2K/W
    m = met * 58.15  # metabolic rate in W/M2
    w = wme * 58.15  # external work in W/M2
    mw = m - w  # internal heat production in the human body
    # calculation of the clothing area factor
    if icl <= 0.078:
        f_cl = 1 + (1.29 * icl)  # ratio of surface clothed body over nude body
    else:
        f_cl = 1.05 + (0.645 * icl)

    # heat transfer coefficient by forced convection
    hcf = 12.1 * np.sqrt(vr)
    hc = hcf  # initialize variable
    taa = tdb + 273
    tra = tr + 273
    t_cla = taa + (35.5 - tdb) / (3.5 * icl + 0.1)

    p1 = icl * f_cl
    p2 = p1 * 3.96
    p3 = p1 * 100
    p4 = p1 * taa
    p5 = (308.7 - 0.028 * mw) + (p2 * (tra / 100.0) ** 4)
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
            raise StopIteration("Max iterations exceeded")

    tcl = 100 * xn - 273

    # heat loss diff. through skin
    hl1 = 3.05 * 0.001 * (5733 - (6.99 * mw) - pa)
    # heat loss by sweating
    if mw > 58.15:
        hl2 = 0.42 * (mw - 58.15)
    else:
        hl2 = 0
    # latent respiration heat loss
    hl3 = 1.7 * 0.00001 * m * (5867 - pa)
    # dry respiration heat loss
    hl4 = 0.0014 * m * (34 - tdb)
    # heat loss by radiation
    hl5 = 3.96 * f_cl * (xn**4 - (tra / 100.0) ** 4)
    # heat loss by convection
    hl6 = f_cl * hc * (tcl - tdb)

    ts = 0.303 * np.exp(-0.036 * m) + 0.028
    _pmv = ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6)

    return _pmv

def calculate_tdb(t_db_x, t_r, v_r, r_h, met, clo_d, pmv_y):
    return (
        _pmv_ppd_optimized(tdb=t_db_x, tr=t_r, vr=v_r, rh=r_h, met=met, clo=clo_d)
        - pmv_y
    )

# Psychrometric(air temperature) of ASHRAE
def psychrometric_ashrae(
    inputs: dict = None,
    model: str = "iso",
    function_selection: str = Functionalities.Default,
    units: str = "SI",
    
):

    p_tdb = float(inputs[ElementsIDs.t_db_input.value])
    tr = float(inputs[ElementsIDs.t_r_input.value])
    vr = float(
        v_relative(  # Ensure vr is scalar
            v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
        )
    )
    rh = float(inputs[ElementsIDs.rh_input.value])
    met = float(inputs[ElementsIDs.met_input.value])
    clo = float(
        clo_dynamic(  # Ensure clo is scalar
            clo=inputs[ElementsIDs.clo_input.value],
            met=inputs[ElementsIDs.met_input.value],
        )
    )
    # save original values for plotting
    if units == UnitSystem.IP.value:
        tdb = round(float(units_converter(tdb=p_tdb)[0]), 1)
        tr = round(float(units_converter(tr=tr)[0]), 1)
        vr = round(float(units_converter(vr=vr)[0]), 1)
    else:
        tdb = p_tdb

    traces = []

    # blue area

    rh_values = np.arange(0, 110, 10)
    tdb_guess = 22
    pmv_list = [-0.5, 0.5]
    tdb_array = np.zeros((len(pmv_list), len(rh_values)))
    for j, pmv_value in enumerate(pmv_list):
        for i, rh_value in enumerate(rh_values):
            solution = fsolve(
                lambda x: calculate_tdb(
                    t_db_x=x,
                    t_r=tr,
                    v_r=vr,
                    r_h=rh_value,
                    met=met,
                    clo_d=clo,
                    pmv_y=pmv_value,
                ),
                tdb_guess,
            )
            tdb_solution = round(solution[0], 1)
            tdb_guess = tdb_solution
            tdb_array[j, i] = float(tdb_solution)

    # calculate hr

    lower_upper_tdb = np.append(tdb_array[0], tdb_array[1][::-1])
    lower_upper_tdb = [
        round(float(value), 1) for value in lower_upper_tdb.tolist()
    ]  # convert to list & round to 1 decimal

    rh_list = np.append(np.arange(0, 110, 10), np.arange(100, -1, -10))


    # define
    lower_upper_hr = []
    for i in range(len(rh_list)):
        lower_upper_hr.append(
            psy_ta_rh(tdb=lower_upper_tdb[i], rh=rh_list[i])["hr"] * 1000
        )

    lower_upper_hr = [
        round(float(value), 1) for value in lower_upper_hr
    ]  # convert to list & round to 1 decimal

    if units == UnitSystem.IP.value:
        lower_upper_tdb = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                lower_upper_tdb,
            )
        )
    
    # grey area
    if model == "ashrae" and function_selection == Functionalities.Compare.value:
            
            met_2, clo_2, tr_2, t_db_2, v_2, rh_2 = compare_get_inputs(inputs)
            
            print("Type of met_2:", type(met_2), "Value:", met_2)
            print("Type of clo_2:", type(clo_2), "Value:", clo_2)
            print("Type of tr_2:", type(tr_2), "Value:", tr_2)
            print("Type of t_db_2:", type(t_db_2), "Value:", t_db_2)
            print("Type of v_2:", type(v_2), "Value:", v_2)
            print("Type of rh_2:", type(rh_2), "Value:", rh_2)

            clo_d_compare = clo_dynamic(clo_2, met_2)
            vr_compare = v_relative(v_2, met_2)
            
           
            vr_2 = vr_compare
            clo_2 = clo_d_compare
             # save original values for plotting
            
            
            if units == UnitSystem.IP.value:

                t_db_2 = round(float(units_converter(tdb=t_db_2)[0]), 1)
                tr_2 = round(float(units_converter(tr=tr_2)[0]), 1)
                vr_2 = round(float(units_converter(vr=vr_2)[0]), 1)
                print("Type of t_db_2:", type(t_db_2), "Value:", t_db_2)
                print("Type of tr_2:", type(tr_2), "Value:", tr_2)
                print("Type of vr_2:", type(vr_2), "Value:", vr_2)
               
            else:
                t_db_2 = t_db_2
            
            
                
            print("Type of t_db_2:", type(t_db_2), "Value:", t_db_2)
            print("Type of tr_2:", type(tr_2), "Value:", tr_2)
            print("Type of vr_2:", type(vr_2), "Value:", vr_2)
            
        
           
            traces = []
    
    
            
            rh_values_2 = np.arange(0, 110, 10)
            tdb_guess_2 = 22
            pmv_list_2 = [-0.5, 0.5]
            tdb_array_2 = np.zeros((len(pmv_list_2), len(rh_values_2)))
            for j, pmv_value in enumerate(pmv_list_2):
                for i, rh_value in enumerate(rh_values_2):
                    solution_2 = fsolve(
                        lambda x2: calculate_tdb(
                            t_db_x=x2,
                            t_r=tr_2,
                            v_r=vr_2,
                            r_h=rh_value,
                            met=met_2,
                            clo_d=clo_2,
                            pmv_y=pmv_value,
                        ),
                        tdb_guess_2,
                    )
                    tdb_solution_2 = round(solution_2[0], 1)
                    tdb_guess_2 = tdb_solution_2
                    tdb_array_2[j, i] = float(tdb_solution_2)
        
            # calculate hr
           
            lower_upper_tdb_2 = np.append(tdb_array_2[0], tdb_array_2[1][::-1])
            lower_upper_tdb_2 = [
                round(float(value), 1) for value in lower_upper_tdb_2.tolist()
            ]  # convert to list & round to 1 decimal
        
            rh_list_2 = np.append(np.arange(0, 110, 10), np.arange(100, -1, -10))
        
        
            # define
            lower_upper_hr_2 = []
            for i in range(len(rh_list_2)):
                lower_upper_hr_2.append(
                    psy_ta_rh(tdb=lower_upper_tdb_2[i], rh=rh_list_2[i])["hr"] * 1000
                )
        
            lower_upper_hr_2 = [
                round(float(value), 1) for value in lower_upper_hr_2
            ]  # convert to list & round to 1 decimal
        
            if units == UnitSystem.IP.value:
                lower_upper_tdb_2 = list(
                    map(
                        lambda x2: round(float(units_converter(tmp=x2, from_units="si")[0]), 1),
                        lower_upper_tdb_2,
                    )
                )
        
            traces.append(
                go.Scatter(
                    x=lower_upper_tdb_2,
                    y=lower_upper_hr_2,
                    mode="lines",
                    line=dict(color="rgba(0,0,0,0)"),
                    fill="toself",
                    fillcolor="rgba(200, 200, 200, 0.7)",
                    showlegend=False,
                    hoverinfo="none",
                )
            )
        
            # current point
            # Red point
        
            psy_results = psy_ta_rh(t_db_2, rh_2)
            hr_2 = round(float(psy_results["hr"]) * 1000, 1)
            t_wb_2 = round(float(psy_results["t_wb"]), 1)
            t_dp_2 = round(float(psy_results["t_dp"]), 1)
            h = round(float(psy_results["h"]) / 1000, 1)
        
            if units == UnitSystem.IP.value:
                t_wb_2 = round(float(units_converter(tmp=t_wb_2, from_units="si")[0]), 1)
                t_dp_2 = round(float(units_converter(tmp=t_dp_2, from_units="si")[0]), 1)
                h = round(float(h / 2.326), 1)  # kJ/kg => btu/lb
                t_db_2 = (t_db_2 * 9/5) + 32
            
            print("Type of hr_2:", type(hr_2), "Value:", hr_2)
            print("Type of t_wb_2:", type(t_wb_2), "Value:", t_wb_2)
            print("Type of t_dp_2:", type(t_dp_2), "Value:", t_dp_2)
            print("Type of h:", type(h), "Value:", h)
            print("Type of t_db_2:", type(t_db_2), "Value:", t_db_2)
            
            
            traces.append(
                go.Scatter(
                    x=[t_db_2],
                    y=[hr_2],
                    mode="markers",
                    marker=dict(
                        color="purple",
                        size=6,
                    ),
                    showlegend=False,
                )
            )


    traces.append(
        go.Scatter(
            x=lower_upper_tdb,
            y=lower_upper_hr,
            mode="lines",
            line=dict(color="rgba(0,0,0,0)"),
            fill="toself",
            fillcolor="rgba(59, 189, 237, 0.7)",
            showlegend=False,
            hoverinfo="none",
        )
    )

    # current point
    # Red point

    psy_results = psy_ta_rh(tdb, rh)
    hr = round(float(psy_results["hr"]) * 1000, 1)
    t_wb = round(float(psy_results["t_wb"]), 1)
    t_dp = round(float(psy_results["t_dp"]), 1)
    h = round(float(psy_results["h"]) / 1000, 1)

    if units == UnitSystem.IP.value:
        t_wb = round(float(units_converter(tmp=t_wb, from_units="si")[0]), 1)
        t_dp = round(float(units_converter(tmp=t_dp, from_units="si")[0]), 1)
        h = round(float(h / 2326), 1)  # kJ/kg => btu/lb
        tdb = p_tdb

    traces.append(
        go.Scatter(
            x=[tdb],
            y=[hr],
            mode="markers",
            marker=dict(
                color="red",
                size=6,
            ),
            showlegend=False,
        )
    )

       

    # lines

    rh_list = np.arange(0, 110, 10, dtype=float).tolist()
    tdb_list = np.linspace(10, 36, 500, dtype=float).tolist()
    if units == UnitSystem.IP.value:
        tdb_list_conv = list(
            map(
                lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                tdb_list,
            )
        )
    else:
        tdb_list_conv = tdb_list

    for rh in rh_list:
        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb_list]
        )  # kg/kg => g/kg
        trace = go.Scatter(
            x=tdb_list_conv,
            y=hr_list,
            mode="lines",
            line=dict(color="grey", width=1),
            hoverinfo="x+y",
            name=f"{rh}% RH",
            showlegend=False,
        )
        traces.append(trace)

    
    
    tdb = inputs[ElementsIDs.t_db_input.value]
    rh = inputs[ElementsIDs.rh_input.value]
    tr = inputs[ElementsIDs.t_r_input.value]

   
    

    

    if units == UnitSystem.SI.value:
        temperature_unit = "°C"
        hr_unit = "g<sub>w</sub>/kg<sub>da</sub>"
        h_unit = "kJ/kg"
        psy_results = psy_ta_rh(tdb, rh)
        t_dp = psy_results.t_dp
        h = psy_results.h/2326
        print("Type of h:", type(h), "Value:", h)
        print("Type of t_dp:", type(t_dp), "Value:", t_dp)
    else:
        temperature_unit = "°F"
        hr_unit = "lb<sub>w</sub>/klb<sub>da</sub>" 
        h_unit = "btu/lb"  
        tdb = (tdb - 32)/1.8
        psy_results = psy_ta_rh(tdb, rh)
        
        
        t_dp = psy_results.t_dp
        h = psy_results.h/2326 * 2.20462
        h = round(h, 1)
        print("Type of h:", type(h), "Value:", h)
        print("Type of t_dp:", type(t_dp), "Value:", t_dp)
    
    if units == UnitSystem.SI.value:
       tdb = tdb
       t_dp = t_dp
    else:
       tdb = tdb * 1.8 + 32
       t_dp = t_dp * 1.8 + 32

         
    #layout
    layout = go.Layout(
        margin=dict(l=10, t=0),
        height=500,
        width=680,
        xaxis=dict(
            title=(
                "Dry-bulb Temperature [°C]"
                if units == UnitSystem.SI.value
                else "operative Temperature [°F]"
            ),
            range=[10, 36] if units == UnitSystem.SI.value else [50, 96.8],
            dtick=2,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
        ),
        yaxis=dict(
            title=(
                "Humidity Ratio [g<sub>w</sub>/kg<sub>da</sub>]"
                if units == UnitSystem.SI.value
                else "Humidity ratio [lb<sub>w</sub>/klb<sub>da</sub>]"  # 保持角标
            ),
            range=[0, 30],
            dtick=5,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
            side="right",
        ),
        annotations=[
            dict(
                x=14 if units == UnitSystem.SI.value else  57,
                y=28,
                xref="x",
                yref="y",
                text=(
                    
                    f"tₜdb: {tdb:.1f} {temperature_unit}<br>"
                    f"rh: {rh:.1f} %<br>"
                    f"Wₐ: {hr} {hr_unit}<br>"
                    f"tₓwb: {t_wb} {temperature_unit}<br>"
                    f"tₓdp: {t_dp:.1f} {temperature_unit}<br>" 
                    f"h: {h:.2f} {h_unit}<br>"  
                ),
                showarrow=False,
                align="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0)",
                font=dict(size=10),
            )
        ],
        showlegend=True,
        plot_bgcolor="white",
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig