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
            f"W<sub>a</sub>: {psy_results.hr*1000:.1f} lb<sub>w</sub>/klb<sub>da</sub><br>"  # g/kg to gr/lb
            f"t<sub>wb</sub>: {psy_results.t_wb:.1f} °F<br>"
            f"t<sub>dp</sub>: {(psy_results.t_dp-32)/1.8:.1f} °F<br>"
            f"h: {psy_results.h / 2326:.1f} btu/lb"  # kJ/kg to btu/lb
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




def psy_ashrae_pmv(
    inputs: dict = None,
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

    #add transparent grid
    x_range = np.linspace(10, 36, 100) if units == UnitSystem.SI.value else np.linspace(50, 96.8, 100)
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
            showlegend=False
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
