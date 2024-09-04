import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Output, Input, no_update, State

from components.charts import chart_example
from components.dropdowns import (
    model_selection,
    chart_selection,
    dd_model,
)
from components.functionality_selection import functionality_selection
from components.input_environmental_personal import input_environmental_personal
from components.my_card import my_card
from components.show_results import display_results
from utils.my_config_file import (
    URLS,
    ElementsIDs,
    Dimensions,
    UnitSystem,
    Models,
)

dash.register_page(__name__, path=URLS.HOME.value)

layout = dmc.Stack(
    [
        dmc.Grid(
            children=[
                dmc.GridCol(
                    model_selection(),
                    # todo we should define the size of the left columns and of the right columns and then create a class and import from there, we should not define them here in the text, see example below
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
                            dmc.Text("Visualization", m="xs", fw=700),
                            html.Div(
                                id="chart-select",
                                children=chart_selection(),
                            ),
                            dcc.Graph(
                                id=ElementsIDs.CHART_CONTAINER.value,
                                figure=chart_example("", ""),
                            ),
                            dmc.Text(id=ElementsIDs.model_note.value),
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
    Input(dd_model["id"], "value"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
)
def update_inputs(selected_model, units_selection):
    if selected_model is None:
        return no_update
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    return input_environmental_personal(selected_model, units)


@callback(
    Output(ElementsIDs.model_note.value, "children"),
    Input(dd_model["id"], "value"),
)
def update_model_note(selected_model):
    if selected_model is None:
        return no_update
    if Models[selected_model].value.model_note:
        return Models[selected_model].value.model_note


@callback(
    Output(ElementsIDs.RESULTS_SECTION.value, "children"),
    Input(dd_model["id"], "value"),
    Input("test-form", "n_clicks"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
    State("test-form", "children"),
    # todo this function should also listen to changes in the variables inputs
)
def update_outputs(selected_model, _, units_selection: str, form_content: dict):
    return display_results(selected_model, form_content, units_selection)
