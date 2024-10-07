import dash
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, no_update, State, ctx, dcc


from components.charts import (
    t_rh_pmv,
    chart_selector,
    adaptive_chart,
    generate_tdb_hr_chart,
    SET_outputs_chart,
    speed_temp_pmv,
    get_heat_losses,
    psy_ashrae_pmv,
    generate_operative_chart,
)

from components.dropdowns import (
    model_selection,
)
from components.functionality_selection import functionality_selection
from components.input_environmental_personal import input_environmental_personal
from components.my_card import my_card
from components.show_results import display_results
from utils.get_inputs import get_inputs
from utils.my_config_file import (
    URLS,
    ElementsIDs,
    Dimensions,
    UnitSystem,
    Models,
    Charts,
    ChartsInfo,
    MyStores,
    Functionalities,
)
import plotly.graph_objects as go
from pythermalcomfort.psychrometrics import psy_ta_rh

dash.register_page(__name__, path=URLS.HOME.value)

layout = dmc.Stack(
    [
        dmc.Grid(
            children=[
                dmc.GridCol(
                    model_selection(),
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                dmc.GridCol(
                    functionality_selection(),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
        dmc.Grid(
            children=[
                my_card(
                    title="Inputs",
                    children=input_environmental_personal(),
                    id=ElementsIDs.INPUT_SECTION.value,
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                my_card(
                    title="Results",
                    children=dmc.Stack(
                        [
                            html.Div(
                                id=ElementsIDs.RESULTS_SECTION.value,
                            ),
                            html.Div(
                                id=ElementsIDs.charts_dropdown.value,
                                children=html.Div(id=ElementsIDs.chart_selected.value),
                            ),
                            html.Div(
                                id=ElementsIDs.CHART_CONTAINER.value,
                            ),
                            dmc.Text(id=ElementsIDs.note_model.value),
                        ],
                    ),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
    ]
)


# Todo adding reflecting value to the url
@callback(
    Output(MyStores.input_data.value, "data"),
    Input(ElementsIDs.inputs_form.value, "n_clicks"),
    Input(ElementsIDs.inputs_form.value, "children"),
    Input(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.met_input.value, "value"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
    Input(ElementsIDs.chart_selected.value, "value"),
    Input(ElementsIDs.functionality_selection.value, "value"),
    State(ElementsIDs.MODEL_SELECTION.value, "value"),
)
def update_store_inputs(
    form_clicks: int,
    form_content: dict,
    clo_value: float,
    met_value: float,
    units_selection: str,
    chart_selected: str,
    functionality_selection: str,
    selected_model: str,
):
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    inputs = get_inputs(selected_model, form_content, units, functionality_selection)

    if ctx.triggered:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_id == ElementsIDs.clo_input.value and clo_value != "":
            inputs[ElementsIDs.clo_input.value] = float(clo_value)
        if triggered_id == ElementsIDs.met_input.value and met_value != "":
            inputs[ElementsIDs.met_input.value] = float(met_value)

    inputs[ElementsIDs.UNIT_TOGGLE.value] = units
    inputs[ElementsIDs.MODEL_SELECTION.value] = selected_model
    inputs[ElementsIDs.chart_selected.value] = chart_selected
    inputs[ElementsIDs.functionality_selection.value] = functionality_selection

    return inputs


# todo get the value from the url
@callback(
    Output(ElementsIDs.INPUT_SECTION.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
    Input(ElementsIDs.functionality_selection.value, "value"),
)
def update_inputs(selected_model, units_selection, function_selection):
    # todo here I should first check if some inputs are already stored in the store
    if selected_model is None:
        return no_update
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    return input_environmental_personal(selected_model, units, function_selection)


@callback(
    Output(ElementsIDs.note_model.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
)
def update_note_model(selected_model):
    if selected_model is None:
        return no_update
    if Models[selected_model].value.note_model:
        return html.Div(
            [
                dmc.Text("Limits of Applicability: ", size="sm", fw=700, span=True),
                dmc.Text(Models[selected_model].value.note_model, size="sm", span=True),
            ]
        )


@callback(
    Output(ElementsIDs.charts_dropdown.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
    Input(ElementsIDs.functionality_selection.value, "value"),
)
def update_note_model(selected_model, function_selection):
    if selected_model is None:
        return no_update
    return chart_selector(
        selected_model=selected_model, function_selection=function_selection
    )


#  double check the calculating method from pythermalcomfort lib, especially the units
last_valid_annotation = None


# @callback(
#     Output(ElementsIDs.CHART_CONTAINER.value, "children"),
#     Input(MyStores.input_data.value, "data"),
#     Input(ElementsIDs.GRAPH_HOVER.value, "hoverData"),
#     State(ElementsIDs.GRAPH_HOVER.value, "figure"),
#     Input(ElementsIDs.functionality_selection.value, "value"),
#     State(MyStores.input_data.value, "data"),
# )
@callback(
    Output(ElementsIDs.GRAPH_HOVER.value, "figure"),
    Input(ElementsIDs.GRAPH_HOVER.value, "hoverData"),
    State(ElementsIDs.GRAPH_HOVER.value, "figure"),
    State(MyStores.input_data.value, "data"),
)
def update_hover_annotation(hover_data, figure, inputs):
    # For ensure tdp never shown as nan value
    global last_valid_annotation

    if (
        hover_data
        and figure
        and "points" in hover_data
        and len(hover_data["points"]) > 0
    ):
        chart_selected = inputs[ElementsIDs.chart_selected.value]

        # not show annotation for adaptive methods
        if chart_selected in [
            Charts.psychrometric.value.name,
            Charts.t_rh.value.name,
            Charts.psychrometric_operative.value.name,
        ]:
            point = hover_data["points"][0]

            if "x" in point and "y" in point:
                t_db = point["x"]
                rh = point["y"]

                # check if y <= 0
                if rh <= 0:
                    if (
                        last_valid_annotation is not None
                        and "annotations" in figure["layout"]
                    ):
                        figure["layout"]["annotations"][0][
                            "text"
                        ] = last_valid_annotation
                    return figure

                # calculations
                psy_results = psy_ta_rh(t_db, rh)
                t_wb_value = psy_results.t_wb
                t_dp_value = psy_results.t_dp
                wa = psy_results.hr * 1000  # convert to g/kgda
                h = psy_results.h / 1000  # convert to kj/kg

                annotation_text = (
                    f"t<sub>db</sub>: {t_db:.1f} °C<br>"
                    f"RH: {rh:.1f} %<br>"
                    f"W<sub>a</sub>: {wa:.1f} g<sub>w</sub>/kg<sub>da</sub><br>"
                    f"t<sub>wb</sub>: {t_wb_value:.1f} °C<br>"
                    f"t<sub>dp</sub>: {t_dp_value:.1f} °C<br>"
                    f"h: {h:.1f} kJ/kg<br>"
                )

                if (
                    "annotations" in figure["layout"]
                    and len(figure["layout"]["annotations"]) > 0
                ):
                    figure["layout"]["annotations"][0]["text"] = annotation_text
            else:
                print("Unexpected hover data structure:", point)

    return figure


@callback(
    Output(ElementsIDs.CHART_CONTAINER.value, "children"),
    Input(MyStores.input_data.value, "data"),
    Input(ElementsIDs.functionality_selection.value, "value"),
)
def update_chart(inputs: dict, function_selection: str):
    selected_model: str = inputs[ElementsIDs.MODEL_SELECTION.value]
    units: str = inputs[ElementsIDs.UNIT_TOGGLE.value]
    chart_selected = inputs[ElementsIDs.chart_selected.value]
    function_selection = inputs[ElementsIDs.functionality_selection.value]

    placeholder = html.Div(
        [
            dmc.Title("Unfortunately this chart has not been implemented yet", order=4),
            dmc.Image(
                src="assets/media/chart_placeholder.png",
            ),
        ]
    )
    image = go.Figure()

    if chart_selected == Charts.t_rh.value.name:
        if (
            selected_model == Models.PMV_EN.name
            and function_selection != Functionalities.Ranges.value
        ):
            image = t_rh_pmv(
                inputs=inputs,
                model="iso",
                function_selection=function_selection,
                units=units,
            )
        elif (
            selected_model == Models.PMV_ashrae.name
            and function_selection == Functionalities.Default.value
        ):
            image = t_rh_pmv(
                inputs=inputs,
                model="ashrae",
                function_selection=function_selection,
                units=units,
            )
    elif chart_selected == Charts.psychrometric.value.name:
        if (
            selected_model == Models.PMV_ashrae.name
            and function_selection == Functionalities.Default.value
        ):
            image = psy_ashrae_pmv(inputs=inputs, model="ashrae")

        elif (
            selected_model == Models.PMV_EN.name
            and function_selection == Functionalities.Default.value
        ):
            image = generate_tdb_hr_chart(inputs=inputs, model="iso", units=units)

    elif chart_selected == Charts.psychrometric_operative.value.name:
        if (
            selected_model == Models.PMV_EN.name
            and function_selection == Functionalities.Default.value
        ):
            use_to = chart_selected == Charts.psychrometric_operative.value.name
        image = generate_operative_chart(inputs=inputs, model="iso")

    elif chart_selected == Charts.set_outputs.value.name:
        if (
            selected_model == Models.PMV_ashrae.name
            and function_selection == Functionalities.Default.value
        ):
            image = SET_outputs_chart(
                inputs=inputs, calculate_ce=False, p_atmospheric=101325, units=units
            )

    elif chart_selected == Charts.wind_temp_chart.value.name:
        if (
            selected_model == Models.PMV_ashrae.name
            and function_selection == Functionalities.Default.value
        ):
            image = speed_temp_pmv(inputs=inputs, model="ashrae", units=units)
    elif chart_selected == Charts.thl_psychrometric.value.name:
        if (
            selected_model == Models.PMV_ashrae.name
            and function_selection == Functionalities.Default.value
        ):
            image = get_heat_losses(inputs=inputs, model="ashrae", units=units)

    if (
        selected_model == Models.Adaptive_EN.name
        and function_selection == Functionalities.Default.value
    ):
        image = adaptive_chart(inputs=inputs, model="iso", units=units)
    if (
        selected_model == Models.Adaptive_ASHRAE.name
        and function_selection == Functionalities.Default.value
    ):
        image = adaptive_chart(inputs=inputs, model="ashrae", units=units)

    note = ""
    chart: ChartsInfo
    for chart in Models[selected_model].value.charts:
        if chart.name == chart_selected:
            note = chart.note_chart

    graph_component = (
        placeholder
        if not image.data
        else dcc.Graph(
            id=ElementsIDs.GRAPH_HOVER.value,
            figure=image,  # Pass the Plotly figure object here
        )
    )

    return dmc.Stack(
        [
            graph_component,
            html.Div(
                [
                    dmc.Text("Note: ", size="sm", fw=700, span=True),
                    dmc.Text(note, size="sm", span=True),
                ]
            ),
        ]
    )


@callback(
    Output(ElementsIDs.RESULTS_SECTION.value, "children"),
    Input(MyStores.input_data.value, "data"),
)
def update_outputs(inputs: dict):
    return display_results(inputs)
