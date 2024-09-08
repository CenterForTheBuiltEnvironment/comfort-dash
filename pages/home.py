import dash
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, no_update, State, ALL

from components.charts import t_rh_pmv, chart_selector
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
)

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


@callback(
    Output(ElementsIDs.INPUT_SECTION.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
)
def update_inputs(selected_model, units_selection):
    if selected_model is None:
        return no_update
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    return input_environmental_personal(selected_model, units)


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
)
def update_note_model(selected_model):
    if selected_model is None:
        return no_update
    return chart_selector(selected_model=selected_model)


@callback(
    Output(ElementsIDs.CHART_CONTAINER.value, "children"),
    Input({"type": "dynamic-input", "index": ALL}, "value"),
    Input(ElementsIDs.chart_selected.value, "value"),
    State(ElementsIDs.MODEL_SELECTION.value, "value"),
    State(ElementsIDs.UNIT_TOGGLE.value, "checked"),
)
def update_chart(
    input_values: list,
    chart_selected: str,
    selected_model: str,
    units_selection: str,
):
    if selected_model is None:
        return no_update

    if chart_selected is None:
        return no_update
    
    model_inputs = Models[selected_model].value.inputs
    form_content = {
        model_input.id: {"value": input_value}
        for model_input, input_value in zip(model_inputs, input_values)
    }
    
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    inputs = get_inputs(selected_model, form_content, units)

    image = html.Div(
        [
            dmc.Title("Unfortunately this chart has not been implemented yet", order=4),
            dmc.Image(
                src="assets/media/chart_placeholder.png",
            ),
        ]
    )

    if chart_selected == Charts.t_rh.value.name:
        if selected_model == Models.PMV_EN.name:
            image = t_rh_pmv(inputs=inputs, model="iso")
        elif selected_model == Models.PMV_ashrae.name:
            image = t_rh_pmv(inputs=inputs, model="ashrae")

    note = ""
    chart: ChartsInfo
    for chart in Models[selected_model].value.charts:
        if chart.name == chart_selected:
            note = chart.note_chart

    return dmc.Stack(
        [
            image,
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
    Input({"type": "dynamic-input", "index": ALL}, "value"),
    State(ElementsIDs.MODEL_SELECTION.value, "value"),
    State(ElementsIDs.UNIT_TOGGLE.value, "checked"),
)
def update_outputs(input_values, selected_model, units_selection: str):
    if selected_model is None or not input_values:
        return no_update
    model_inputs = Models[selected_model].value.inputs
    form_content = {
        model_input.id: {"value": input_value}
        for model_input, input_value in zip(model_inputs, input_values)
    }
    return display_results(selected_model, form_content, units_selection)
