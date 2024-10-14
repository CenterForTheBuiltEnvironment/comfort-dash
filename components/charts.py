import numpy as np
import pandas as pd
import math
import plotly.graph_objs as go
from pythermalcomfort.psychrometrics import psy_ta_rh, p_sat, t_dp, t_wb, enthalpy, t_o
from pythermalcomfort import set_tmp, two_nodes
from pythermalcomfort.models import pmv, adaptive_en, adaptive_ashrae, cooling_effect
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
from scipy.optimize import fsolve
from decimal import Decimal, ROUND_HALF_UP


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

def find_tdb_for_pmv(
    target_pmv,
    tr,
    vr,
    rh,
    met,
    clo,
    wme=0,
    standard="ISO",
    units="SI",
    tol=1e-2,
    max_iter=100,
):

    if units == UnitSystem.SI.value:
        low, high = 10, 40
    else:
        low, high = 50, 96.8
    iterations = 0

    while iterations < max_iter:
        t_db_guess = (low + high) / 2
        try:
            pmv_value = pmv(
                tdb=t_db_guess,
                tr=tr,
                vr=vr,
                rh=rh,
                met=met,
                clo=clo,
                wme=wme,
                standard=standard,
                units=units,
                limit_inputs=False,
            )
        except Exception as e:
            print(f"Error during PMV calculation: {e}")
            pmv_value = np.nan

        if abs(pmv_value - target_pmv) < tol:
            return round(t_db_guess, 2)
        elif pmv_value < target_pmv:
            low = t_db_guess
        else:
            high = t_db_guess

        iterations += 1

    raise ValueError(
        "Unable to find suitable t_db value within maximum number of iterations"
    )


def psy_pmv(
    inputs: dict = None,
    model: str = "ASHRAE",
    units: str = "SI",
):

    p_tdb = float(inputs[ElementsIDs.t_db_input.value])
    tr = float(inputs[ElementsIDs.t_r_input.value])
    vr = float(
        v_relative(  # Ensure vr is scalar
            v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
        )
    )
    p_rh = float(inputs[ElementsIDs.rh_input.value])
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

    # if model is PMV-ASHRAE plot blue area, else plot green areas
    rh_values = np.arange(0, 110, 10)
    if model == "ASHRAE":
        pmv_targets = [-0.5, 0.5]
    else:
        pmv_targets = [-0.7, -0.5, -0.2, 0.2, 0.5, 0.7]
    tdb_array = np.zeros((len(pmv_targets), len(rh_values)))

    for j, pmv_target in enumerate(pmv_targets):
        for i, rh_value in enumerate(rh_values):
            tdb_solution = find_tdb_for_pmv(
                target_pmv=pmv_target,
                tr=tr,
                vr=vr,
                rh=rh_value,
                met=met,
                clo=clo,
                standard=model,
            )
            tdb_array[j, i] = tdb_solution

    # calculate hr
    rh_list = np.append(np.arange(0, 110, 10), np.arange(100, -1, -10))
    if model == "ASHRAE":
        lower_upper_tdb = np.append(tdb_array[0], tdb_array[1][::-1])
        lower_upper_tdb = [
            round(float(value), 1) for value in lower_upper_tdb.tolist()
        ]  # convert to list & round to 1 decimal
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
    else:
        iii_lower_upper_tdb = np.append(tdb_array[0], tdb_array[5][::-1])
        ii_lower_upper_tdb = np.append(tdb_array[1], tdb_array[4][::-1])
        i_lower_upper_tdb = np.append(tdb_array[2], tdb_array[3][::-1])
        iii_lower_upper_tdb = [
            round(float(value), 1) for value in iii_lower_upper_tdb.tolist()
        ]  # convert to list & round to 1 decimal
        ii_lower_upper_tdb = [
            round(float(value), 1) for value in ii_lower_upper_tdb.tolist()
        ]  # convert to list & round to 1 decimal
        i_lower_upper_tdb = [
            round(float(value), 1) for value in i_lower_upper_tdb.tolist()
        ]  # convert to list & round to 1 decimal
        # define
        iii_lower_upper_hr = []
        ii_lower_upper_hr = []
        i_lower_upper_hr = []
        for i in range(len(rh_list)):
            iii_lower_upper_hr.append(
                psy_ta_rh(tdb=iii_lower_upper_tdb[i], rh=rh_list[i])["hr"] * 1000
            )
            ii_lower_upper_hr.append(
                psy_ta_rh(tdb=ii_lower_upper_tdb[i], rh=rh_list[i])["hr"] * 1000
            )
            i_lower_upper_hr.append(
                psy_ta_rh(tdb=i_lower_upper_tdb[i], rh=rh_list[i])["hr"] * 1000
            )

        iii_lower_upper_hr = [
            round(float(value), 1) for value in iii_lower_upper_hr
        ]  # convert to list & round to 1 decimal
        ii_lower_upper_hr = [
            round(float(value), 1) for value in ii_lower_upper_hr
        ]  # convert to list & round to 1 decimal
        i_lower_upper_hr = [
            round(float(value), 1) for value in i_lower_upper_hr
        ]  # convert to list & round to 1 decimal

        if units == UnitSystem.IP.value:
            iii_lower_upper_tdb = list(
                map(
                    lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                    iii_lower_upper_tdb,
                )
            )
            ii_lower_upper_tdb = list(
                map(
                    lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                    ii_lower_upper_tdb,
                )
            )
            i_lower_upper_tdb = list(
                map(
                    lambda x: round(float(units_converter(tmp=x, from_units="si")[0]), 1),
                    i_lower_upper_tdb,
                )
            )

        # category III
        traces.append(
            go.Scatter(
                x=iii_lower_upper_tdb,
                y=iii_lower_upper_hr,
                mode="lines",
                line=dict(color="rgba(0,0,0,0)"),
                fill="toself",
                fillcolor="rgba(28,128,28,0.2)",
                showlegend=False,
                hoverinfo="none",
            )
        )
        # category II
        traces.append(
            go.Scatter(
                x=ii_lower_upper_tdb,
                y=ii_lower_upper_hr,
                mode="lines",
                line=dict(color="rgba(0,0,0,0)"),
                fill="toself",
                fillcolor="rgba(28,128,28,0.3)",
                showlegend=False,
                hoverinfo="none",
            )
        )
        # category I
        traces.append(
            go.Scatter(
                x=i_lower_upper_tdb,
                y=i_lower_upper_hr,
                mode="lines",
                line=dict(color="rgba(0,0,0,0)"),
                fill="toself",
                fillcolor="rgba(28,128,28,0.4)",
                showlegend=False,
                hoverinfo="none",
            )
        )

    # current point
    # Red point
    psy_results = psy_ta_rh(tdb, p_rh)
    hr = round(float(psy_results["hr"]) * 1000, 1)
    t_wb = round(float(psy_results["t_wb"]), 1)
    t_dp = round(float(psy_results["t_dp"]), 1)
    h = round(float(psy_results["h"]) / 1000, 1)

    if units == UnitSystem.IP.value:
        t_wb = round(float(units_converter(tmp=t_wb, from_units="si")[0]), 1)
        t_dp = round(float(units_converter(tmp=t_dp, from_units="si")[0]), 1)
        h = round(float(h / 2.326), 1)  # kJ/kg => btu/lb
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
            hoverinfo="none",
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
            hoverinfo="none",
            name=f"{rh}% RH",
            showlegend=False,
        )
        traces.append(trace)

    # add transparent grid
    x_range = (
        np.linspace(10, 36, 100)
        if units == UnitSystem.SI.value
        else np.linspace(50, 96.8, 100)
    )
    y_range = np.linspace(0, 30, 100)
    xx, yy = np.meshgrid(x_range, y_range)

    traces.append(
        go.Scatter(
            x=xx.flatten(),
            y=yy.flatten(),
            mode="markers",
            marker=dict(size=2, color="rgba(0,0,0,0)"),
            hoverinfo="x+y",
            name="Interactive Hover Area",
            showlegend=False,
        )
    )

    if units == UnitSystem.SI.value:
        temperature_unit = "°C"
        hr_unit = "g<sub>w</sub>/kg<sub>da</sub>"
        h_unit = "kJ/kg"
    else:
        temperature_unit = "°F"
        hr_unit = "lb<sub>w</sub>/klb<sub>da</sub>"
        h_unit = "btu/lb"

    # layout
    layout = go.Layout(
        hovermode="closest",
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
                else "Humidity ratio [lb<sub>w</sub>/klb<sub>da</sub>]"
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
                x=14 if units == UnitSystem.SI.value else 57.2,
                y=28,
                xref="x",
                yref="y",
                text=(
                    f"t<sub>db</sub>: {tdb:.1f} {temperature_unit}<br>"
                    f"rh: {p_rh:.1f} %<br>"
                    f"W<sub>a</sub>: {hr} {hr_unit}<br>"
                    f"t<sub>wb</sub>: {t_wb} {temperature_unit}<br>"
                    f"t<sub>dp</sub>: {t_dp} {temperature_unit}<br>"
                    f"h: {h} {h_unit}"
                ),
                showarrow=False,
                align="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0)",
                font=dict(size=14),
            )
        ],
        showlegend=True,
        plot_bgcolor="white",
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig
