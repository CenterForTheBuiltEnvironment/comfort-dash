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


from pythermalcomfort.models import adaptive_en, pmv


import plotly.graph_objects as go


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
            title=(
                "Outdoor Running Mean Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Prevailing Mean Outdoor Temperature [°F]"
            ),
            range=[10, 30] if model == "iso" else [10, 33.5],
            dtick=2 if units == UnitSystem.SI.value else 5,
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1.5,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="lightgray",
            mirror=True,
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
            gridwidth=1.5,
            ticks="outside",
            ticklen=5,
            showline=True,
            linewidth=1.5,
            linecolor="lightgray",
            mirror=True,
        ),
        legend=dict(x=0.8, y=1),
        showlegend=False,
        # plot_bgcolor="white",
        template="plotly_white",
        # margin=dict(l=40, r=40, t=40, b=40),
        width=700,
        height=525,
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


def calculate_relative_humidity(rh, tdb, hr):
    return 0.62198 * (rh / 100 * p_sat(tdb)) / (101325 - (rh / 100 * p_sat(tdb))) - hr


# calculate the parameters of the chart
def calculate_chart_parameters(tem_dry_bulb, humidity_ratio):
    """
    param tem_dry_bulb: ℃
    param humidity_ratio: g/kg
    """
    # kg/kg，need / 1000
    solution = fsolve(
        lambda x: calculate_relative_humidity(
            rh=x, tdb=tem_dry_bulb, hr=humidity_ratio / 1000
        ),
        1,
    )
    relative_humidity = solution[0]  # %
    wet_bulb_temp = t_wb(tem_dry_bulb, relative_humidity)  # ℃
    dew_point_temp = t_dp(tem_dry_bulb, relative_humidity)  # ℃
    h = enthalpy(tem_dry_bulb, humidity_ratio / 1000) / 1000  # J/kg ==> kJ/kg
    return {
        "tdb": tem_dry_bulb,
        "rh": relative_humidity,
        "wa": humidity_ratio,
        "twb": wet_bulb_temp,
        "tdp": dew_point_temp,
        "h": h,
    }


def generate_tdb_hr_chart(
    inputs: dict = None,
    model: str = "iso",
    units: str = "SI",
):

    p_tdb = inputs[ElementsIDs.t_db_input.value]
    p_tr = inputs[ElementsIDs.t_r_input.value]
    p_v = inputs[ElementsIDs.v_input.value]
    p_rh = inputs[ElementsIDs.rh_input.value]
    p_met = inputs[ElementsIDs.met_input.value]
    p_clo_d = inputs[ElementsIDs.clo_input.value]
    p_t_running_mean = inputs[ElementsIDs.t_r_input.value]

    traces = []

    # green area
    rh = np.arange(0, 101, 20)
    pmv_list = [-0.7, -0.5, -0.2, 0.2, 0.5, 0.7]
    v_r = v_relative(v=p_v, met=p_met)
    tdb_dict = {}
    for j in range(len(pmv_list)):
        tdb_dict[j] = []
        for i in range(len(rh)):
            solution = fsolve(
                lambda x: calculate_tdb(
                    t_db_x=x,
                    t_r=p_tr,
                    v_r=v_r,
                    r_h=rh[i],
                    met=p_met,
                    clo_d=p_clo_d,
                    pmv_y=pmv_list[j],
                ),
                22,
            )
            tdb_solution = Decimal(solution[0]).quantize(
                Decimal("0.0"), rounding=ROUND_HALF_UP
            )  # ℃
            tdb_dict[j].append(float(tdb_solution))

    # hr
    iii_lower_upper_tdb = np.append(np.array(tdb_dict[0]), np.array(tdb_dict[5])[::-1])
    ii_lower_upper_tdb = np.append(np.array(tdb_dict[1]), np.array(tdb_dict[4])[::-1])
    i_lower_upper_tdb = np.append(np.array(tdb_dict[2]), np.array(tdb_dict[3])[::-1])
    rh_list = np.append(np.arange(0, 101, 20), np.arange(100, -1, -20))
    # define
    iii_lower_upper_hr = []
    ii_lower_upper_hr = []
    i_lower_upper_hr = []
    for i in range(len(rh_list)):
        iii_lower_upper_hr.append(
            psy_ta_rh(tdb=iii_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )
        ii_lower_upper_hr.append(
            psy_ta_rh(tdb=ii_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )
        i_lower_upper_hr.append(
            psy_ta_rh(tdb=i_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )

    # traces[0]
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

    # Red point
    red_point_x = p_tdb
    red_point_y = (
        psy_ta_rh(tdb=p_tdb, rh=p_rh, p_atm=101325)["hr"] * 1000
    )  # kg/kg => g/kg
    traces.append(
        go.Scatter(
            x=[red_point_x],
            y=[red_point_y],
            mode="markers",
            marker=dict(
                color="red",
                size=4,
            ),
            showlegend=False,
        )
    )

    # line
    rh_list = np.arange(0, 101, 10)
    tdb = np.linspace(10, 36, 500)
    for rh in rh_list:
        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb]
        )  # kg/kg => g/kg
        trace = go.Scatter(
            x=tdb,
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
    psy_results = psy_ta_rh(tdb, rh)

    ##title
    layout = go.Layout(
        title="Psychrometric (air temperature)",
        xaxis=dict(
            title=(
                "Dry-bulb Temperature [°C]"
                if units == UnitSystem.SI.value
                else "Dry-bulb Temperature [°F]"
            ),
            range=[10, 36],
            dtick=2,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
        ),
        yaxis=dict(
            title="Humidity Ratio [g<sub>w</sub>/kg<sub>da</sub>]",
            range=[0, 30],
            dtick=5,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
            side="right",
        ),
        showlegend=True,
        plot_bgcolor="white",
        annotations=[
            dict(
                x=14,
                y=28,
                xref="x",
                yref="y",
                text=(
                    f"t<sub>db</sub>: {tdb:.1f} °C<br>"
                    f"rh: {rh:.1f} %<br>"
                    f"W<sub>a</sub>: {psy_results.hr * 1000:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
                    f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °C<br>"
                    f"t<sub>dp</sub>: {psy_results.t_dp:.1f} °C<br>"
                    f"h: {psy_results.h / 1000:.1f} kJ/kg"
                ),
                showarrow=False,
                align="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0)",
                font=dict(size=14),
            )
        ],
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig


def calculate_operative_temperature(tdb, tr, v):
    return (tdb * np.sqrt(10 * v) + tr) / (1 + np.sqrt(10 * v))


# calculate tdb by to value (tdb == tr)
def calculate_tdb_by_to(t_db_x, t_r, v_r, r_h, met, clo_d, pmv_y):
    return (
        _pmv_ppd_optimized(tdb=t_db_x, tr=t_r, vr=v_r, rh=r_h, met=met, clo=clo_d)
        - pmv_y
    )


# calculate tdb, tdb is the x input，pmv is y output
def calculate_tdb(t_db_x, t_r, v_r, r_h, met, clo_d, pmv_y):
    return (
        _pmv_ppd_optimized(tdb=t_db_x, tr=t_r, vr=v_r, rh=r_h, met=met, clo=clo_d)
        - pmv_y
    )


# calculate relative humidity by dry bulb temperature, humidity ratio
def calculate_relative_humidity(rh, tdb, hr):
    return 0.62198 * (rh / 100 * p_sat(tdb)) / (101325 - (rh / 100 * p_sat(tdb))) - hr


def generate_operative_chart(
    inputs: dict = None,
    model: str = "iso",
    units: str = "SI",
):

    p_tdb = inputs[ElementsIDs.t_db_input.value]
    p_tr = inputs[ElementsIDs.t_r_input.value]
    p_v = inputs[ElementsIDs.v_input.value]
    p_rh = inputs[ElementsIDs.rh_input.value]
    p_met = inputs[ElementsIDs.met_input.value]
    p_clo_d = inputs[ElementsIDs.clo_input.value]
    p_t_running_mean = inputs[ElementsIDs.t_r_input.value]

    traces = []

    # green area
    rh = np.arange(0, 101, 10)
    pmv_list = [-0.7, -0.5, -0.2, 0.2, 0.5, 0.7]
    v_r = v_relative(v=p_v, met=p_met)
    tdb_dict = {}
    for j in range(len(pmv_list)):
        tdb_dict[j] = []
        for i in range(len(rh)):
            solution = fsolve(
                lambda x: calculate_tdb(
                    t_db_x=x,
                    t_r=x,
                    v_r=v_r,
                    r_h=rh[i],
                    met=p_met,
                    clo_d=p_clo_d,
                    pmv_y=pmv_list[j],
                ),
                22,
            )
            tdb_solution = Decimal(solution[0]).quantize(
                Decimal("0.0"), rounding=ROUND_HALF_UP
            )  # ℃
            tdb_dict[j].append(float(tdb_solution))

    # hr

    iii_lower_upper_tdb = np.append(np.array(tdb_dict[0]), np.array(tdb_dict[5])[::-1])
    ii_lower_upper_tdb = np.append(np.array(tdb_dict[1]), np.array(tdb_dict[4])[::-1])
    i_lower_upper_tdb = np.append(np.array(tdb_dict[2]), np.array(tdb_dict[3])[::-1])
    rh_list = np.append(np.arange(0, 101, 10), np.arange(100, -1, -10))
    # define
    iii_lower_upper_hr = []
    ii_lower_upper_hr = []
    i_lower_upper_hr = []
    for i in range(len(rh_list)):
        iii_lower_upper_hr.append(
            psy_ta_rh(tdb=iii_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )
        ii_lower_upper_hr.append(
            psy_ta_rh(tdb=ii_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )
        i_lower_upper_hr.append(
            psy_ta_rh(tdb=i_lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"]
            * 1000
        )

    # traces[0]
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
    # traces[1]
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
    # traces[2]
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

    # red point，based on air temperature [℃] and relative humidity [%]
    red_point = [0, 0]
    red_point[0] = p_tdb
    red_point[1] = psy_ta_rh(p_tdb, p_rh, p_atm=101325)["hr"] * 1000  # kg/kg ==> g/kg
    # traces[3]
    traces.append(
        go.Scatter(
            x=[red_point[0]],
            y=[red_point[1]],
            mode="markers",
            marker=dict(
                color="red",
                size=4,
            ),
            # name='point',
            showlegend=False,
        )
    )

    # line
    rh_list = np.arange(0, 101, 10)
    tdb = np.linspace(10, 36, 500)
    # traces[5-15]
    # based on rh%
    for rh in rh_list:
        # humidity ratio list

        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb]
        )  # kg/kg => g/kg
        trace = go.Scatter(
            x=tdb,
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
    psy_results = psy_ta_rh(tdb, rh)

    # layout
    layout = go.Layout(
        title="Psychrometric (operative temperature)",
        xaxis=dict(
            title=(
                "operative Temperature [°C]"
                if units == UnitSystem.SI.value
                else "operative Temperature [°F]"
            ),
            range=[10, 36],
            dtick=2,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
        ),
        yaxis=dict(
            title="Humidity Ratio [g<sub>w</sub>/kg<sub>da</sub>]",
            range=[0, 30],
            dtick=5,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
            side="right",
        ),
        showlegend=True,
        plot_bgcolor="white",
        annotations=[
            dict(
                x=14,
                y=28,
                xref="x",
                yref="y",
                text=(
                    f"t<sub>db</sub>: {tdb:.1f} °C<br>"
                    f"rh: {rh:.1f} %<br>"
                    f"W<sub>a</sub>: {psy_results.hr * 1000:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
                    f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °C<br>"
                    f"t<sub>dp</sub>: {psy_results.t_dp:.1f} °C<br>"
                    f"h: {psy_results.h / 1000:.1f} kJ/kg"
                ),
                showarrow=False,
                align="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0)",
                font=dict(size=14),
            )
        ],
    )

    fig = go.Figure(data=traces, layout=layout)

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
    # Add hover area to allow hover interaction

    x_range = np.linspace(10, 40, 100)

    if units == UnitSystem.IP.value:  # The X-axis range of gridlines in the IP state
        x_range = np.linspace(50, 100, 100)

    y_range = np.linspace(0, 100, 100)
    xx, yy = np.meshgrid(x_range, y_range)
    fig.add_trace(
        go.Scatter(
            x=xx.flatten(),
            y=yy.flatten(),
            mode="markers",
            marker=dict(color="rgba(0,0,0,0)"),
            hoverinfo="x+y",
            name="Interactive Hover Area",
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
                hoverinfo="skip",
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
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[t_db_2],
                y=[rh_2],
                mode="markers",
                marker=dict(color="blue", size=8),
                name="Compare Input",
                hoverinfo="skip",
            )
        )

    tdb = inputs[ElementsIDs.t_db_input.value]
    rh = inputs[ElementsIDs.rh_input.value]
    tr = inputs[ElementsIDs.t_r_input.value]
    psy_results = psy_ta_rh(tdb, rh)

    if units == UnitSystem.SI.value:
        annotation_text = (
            f"t<sub>db</sub>: {tdb:.1f} °C<br>"
            f"rh: {rh:.1f} %<br>"
            f"W<sub>a</sub>: {psy_results.hr*1000:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
            f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °C<br>"
            f"t<sub>dp</sub>: {psy_results.t_dp:.1f} °C<br>"
            f"h: {psy_results.h / 1000:.1f} kJ/kg"
        )
        annotation_x = 32  # x coordinates in SI units
        annotation_y = 86  # Y-coordinate of relative humidity
    elif units == UnitSystem.IP.value:
        annotation_text = (
            f"t<sub>db</sub>: {tdb:.1f} °F<br>"
            f"rh: {rh:.1f} %<br>"
            f"W<sub>a</sub>: {psy_results.hr*1000:.1f} gr<sub>w</sub>/lb<sub>da</sub><br>"  # g/kg to gr/lb
            f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °F<br>"
            f"t<sub>dp</sub>: {(psy_results.t_dp-32)/1.8:.1f} °F<br>"
            f"h: {psy_results.h / 2326:.1f} BTU/lb"  # kJ/kg to BTU/lb
        )
        annotation_x = 90  # x coordinates in IP units
        annotation_y = 86  # Y-coordinate of relative humidity (unchanged)

    fig.add_annotation(
        x=annotation_x,  # Dynamically adjust the x position of a comment
        y=annotation_y,  # The y coordinates remain the same
        xref="x",
        yref="y",
        text=annotation_text,
        showarrow=False,
        align="left",
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=14),
    )

    fig.update_layout(
        yaxis=dict(title="Relative Humidity [%]", range=[0, 100], dtick=10),
        xaxis=dict(
            title=(
                "Dry-bulb Temperature (°C)"
                if units == UnitSystem.SI.value
                else "Dry-bulb Temperature [°F]"
            ),
            range=[10, 36] if units == UnitSystem.SI.value else [50, 100],
            dtick=2 if units == UnitSystem.SI.value else 5,
        ),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="closest",
        hoverdistance=5,
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0, 0, 0, 0.2)")

    return fig


def speed_temp_pmv(
    inputs: dict = None,
    model: str = "iso",
    units: str = "SI",
):
    results = []
    met, clo, tr, t_db, v, rh = get_inputs(inputs)
    clo_d = clo_dynamic(clo, met)
    vr = v_relative(v, met)
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

            try:
                temp = optimize.brentq(function, 10, 40)
                results.append(
                    {
                        "vr": vr,
                        "temp": temp,
                        "pmv_limit": pmv_limit,
                    }
                )

            except ValueError:
                continue

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
            fillcolor="rgba(59, 189, 237, 0.7)",
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
        xaxis_title=(
            "Operative Temperature [°C]"
            if units == UnitSystem.SI.value
            else "Operative Temperature [°F]"
        ),
        # x title
        yaxis_title=(
            "Relative Air Speed [m/s]"
            if units == UnitSystem.SI.value
            else "Relative Air Speed [fpm]"
        ),
        # y title
        template="plotly_white",
        width=700,
        height=700,
        xaxis=dict(
            range=[20, 34] if units == UnitSystem.SI.value else [68, 92],  # x range
            tickmode="linear",
            tick0=20 if units == UnitSystem.SI.value else 68,
            dtick=2,
            linecolor="lightgrey",
            gridcolor="lightgray",
            showgrid=True,
            mirror=True,
        ),
        yaxis=dict(
            range=[0.0, 1.2] if units == UnitSystem.SI.value else [0, 240],  # y range
            tickmode="linear",
            tick0=0.0,
            dtick=0.1 if units == UnitSystem.SI.value else 20,
            linecolor="lightgrey",
            gridcolor="lightgray",
            showgrid=True,
            mirror=True,
        ),
    )
    return fig


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
        width=700,
        height=700,
    )

    return fig


def psy_ashrae_pmv_operative(
    inputs: dict = None,
    model: str = "ashrae",
    units: str = "SI",
):

    p_tdb = inputs[ElementsIDs.t_db_input.value]
    p_tr = inputs[ElementsIDs.t_r_input.value]
    p_v = inputs[ElementsIDs.v_input.value]
    p_rh = inputs[ElementsIDs.rh_input.value]
    p_met = inputs[ElementsIDs.met_input.value]
    p_clo_d = inputs[ElementsIDs.clo_input.value]
    p_t_running_mean = inputs[ElementsIDs.t_r_input.value]

    traces = []

    # green area
    rh = np.arange(0, 101, 10)
    pmv_list = [-0.5, 0.5]
    v_r = v_relative(v=p_v, met=p_met)
    tdb_dict = {}
    for j in range(len(pmv_list)):
        tdb_dict[j] = []
        for i in range(len(rh)):
            solution = fsolve(
                lambda x: calculate_tdb(
                    t_db_x=x,
                    t_r=x,
                    v_r=v_r,
                    r_h=rh[i],
                    met=p_met,
                    clo_d=p_clo_d,
                    pmv_y=pmv_list[j],
                ),
                22,
            )
            tdb_solution = Decimal(solution[0]).quantize(
                Decimal("0.0"), rounding=ROUND_HALF_UP
            )  # ℃
            tdb_dict[j].append(float(tdb_solution))

    # hr

    lower_upper_tdb = np.append(np.array(tdb_dict[0]), np.array(tdb_dict[1])[::-1])
    rh_list = np.append(np.arange(0, 101, 10), np.arange(100, -1, -10))
    # define
    lower_upper_hr = []

    for i in range(len(rh_list)):
        lower_upper_hr.append(
            psy_ta_rh(tdb=lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"] * 1000
        )

    # traces[0]
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

    # red point，based on air temperature [℃] and relative humidity [%]
    red_point = [0, 0]
    red_point[0] = p_tdb
    red_point[1] = psy_ta_rh(p_tdb, p_rh, p_atm=101325)["hr"] * 1000  # kg/kg ==> g/kg
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
            # name='point',
            showlegend=False,
        )
    )

    # line
    rh_list = np.arange(0, 101, 10)
    tdb = np.linspace(10, 36, 500)
    # traces[5-15]
    # based on rh%
    for rh in rh_list:
        # humidity ratio list

        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb]
        )  # kg/kg => g/kg
        trace = go.Scatter(
            x=tdb,
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
    psy_results = psy_ta_rh(tdb, rh)

    # layout
    layout = go.Layout(
        title="Psychrometric (operative temperature)",
        xaxis=dict(
            title=(
                "operative Temperature [°C]"
                if units == UnitSystem.SI.value
                else "operative Temperature [°F]"
            ),
            range=[10, 36],
            dtick=2,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
        ),
        yaxis=dict(
            title="Humidity Ratio [g<sub>w</sub>/kg<sub>da</sub>]",
            range=[0, 30],
            dtick=5,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
            side="right",
        ),
        showlegend=True,
        plot_bgcolor="white",
        annotations=[
            dict(
                x=14,
                y=28,
                xref="x",
                yref="y",
                text=(
                    f"t<sub>db</sub>: {tdb:.1f} °C<br>"
                    f"rh: {rh:.1f} %<br>"
                    f"W<sub>a</sub>: {psy_results.hr * 1000:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
                    f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °C<br>"
                    f"t<sub>dp</sub>: {psy_results.t_dp:.1f} °C<br>"
                    f"h: {psy_results.h / 1000:.1f} kJ/kg"
                ),
                showarrow=False,
                align="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0)",
                font=dict(size=14),
            )
        ],
    )

    fig = go.Figure(data=traces, layout=layout)

    return fig


def psy_ashrae_pmv(
    inputs: dict = None,
    model: str = "ashrae",
    units: str = "SI",
):

    p_tdb = inputs[ElementsIDs.t_db_input.value]
    p_tr = inputs[ElementsIDs.t_r_input.value]
    p_v = inputs[ElementsIDs.v_input.value]
    p_rh = inputs[ElementsIDs.rh_input.value]
    p_met = inputs[ElementsIDs.met_input.value]
    p_clo_d = inputs[ElementsIDs.clo_input.value]
    p_t_running_mean = inputs[ElementsIDs.t_r_input.value]

    traces = []

    # blue area
    rh = np.arange(0, 110, 10)
    pmv_list = [-0.5, 0.5]
    v_r = v_relative(v=p_v, met=p_met)
    tdb_dict = {}
    for j in range(len(pmv_list)):
        tdb_dict[j] = []
        for i in range(len(rh)):
            solution = fsolve(
                lambda x: calculate_tdb(
                    t_db_x=x,
                    t_r=p_tr,
                    v_r=v_r,
                    r_h=rh[i],
                    met=p_met,
                    clo_d=p_clo_d,
                    pmv_y=pmv_list[j],
                ),
                22,
            )
            tdb_solution = Decimal(solution[0]).quantize(
                Decimal("0.0"), rounding=ROUND_HALF_UP
            )  # ℃
            tdb_dict[j].append(float(tdb_solution))

    # calculate hr
    lower_upper_tdb = np.append(np.array(tdb_dict[0]), np.array(tdb_dict[1])[::-1])

    rh_list = np.append(np.arange(0, 110, 10), np.arange(100, -1, -10))
    # define
    lower_upper_hr = []
    for i in range(len(rh_list)):
        lower_upper_hr.append(
            psy_ta_rh(tdb=lower_upper_tdb[i], rh=rh_list[i], p_atm=101325)["hr"] * 1000
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
    red_point_x = p_tdb
    red_point_y = (
        psy_ta_rh(tdb=p_tdb, rh=p_rh, p_atm=101325)["hr"] * 1000
    )  # kg/kg => g/kg
    traces.append(
        go.Scatter(
            x=[red_point_x],
            y=[red_point_y],
            mode="markers",
            marker=dict(
                color="red",
                size=6,
            ),
            showlegend=False,
        )
    )

    # lines
    rh_list = np.arange(0, 110, 10)
    tdb = np.linspace(10, 36, 500)
    for rh in rh_list:
        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb]
        )  # kg/kg => g/kg
        trace = go.Scatter(
            x=tdb,
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
    psy_results = psy_ta_rh(tdb, rh)

    # layout
    layout = go.Layout(
        title="Psychrometric (air temperature)",
        xaxis=dict(
            title=(
                "Dry-bulb Temperature [°C]"
                if units == UnitSystem.SI.value
                else "operative Temperature [°F]"
            ),
            range=[10, 36],
            dtick=2,
            showgrid=True,
            showline=True,
            linewidth=1.5,
            linecolor="lightgrey",
        ),
        yaxis=dict(
            title="Humidity Ratio [g<sub>w</sub>/kg<sub>da</sub>]",
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
                x=14,
                y=28,
                xref="x",
                yref="y",
                text=(
                    f"t<sub>db</sub>: {tdb:.1f} °C<br>"
                    f"rh: {rh:.1f} %<br>"
                    f"W<sub>a</sub>: {psy_results.hr * 1000:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
                    f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °C<br>"
                    f"t<sub>dp</sub>: {psy_results.t_dp:.1f} °C<br>"
                    f"h: {psy_results.h / 1000:.1f} kJ/kg"
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
            clo=inputs[ElementsIDs.clo_input.value], met=met
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
        width=700,
        height=700,
    )
    return fig
