import dash
import dash_mantine_components as dmc

from components.charts import chart_example
from components.functionality_selection import functionality_selection
from components.input_environmental_personal import input_environmental_personal
from components.dropdowns import (
    model_selection,
    chart_selection,
    dd_model,
)
from components.my_card import my_card
from utils.my_config_file import (
    URLS,
    ElementsIDs,
    ModelChartDescription,
    Dimensions,
    Models,
)
from dash import html, dcc, callback, Output, Input, no_update, State
from pythermalcomfort.models import pmv_ppd

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
                    title="Results and Visualization",
                    children=dmc.Stack(
                        [
                            html.Div(
                                id="chart-select",
                                children=chart_selection(),
                            ),
                            html.Div(
                                id=ElementsIDs.RESULTS_SECTION.value,
                            ),
                            dcc.Graph(
                                id=ElementsIDs.CHART_CONTAINER.value,
                                figure=chart_example("", ""),
                            ),
                            dmc.GridCol(
                                children=dmc.Text(
                                    [
                                        html.Strong(ModelChartDescription.note.value),
                                        ModelChartDescription.psy_air_temp_des_1.value,
                                        dmc.Space(h=20),
                                        ModelChartDescription.psy_air_temp_des_2.value,
                                    ],
                                ),
                            ),
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
def update_inputs(selected_model, is_ip):
    if selected_model is None:
        return no_update
    units = "IP" if is_ip else "SI"
    return input_environmental_personal(selected_model, units)


@callback(
    Output(ElementsIDs.RESULTS_SECTION.value, "children"),
    Input(dd_model["id"], "value"),
    Input("test-form", "n_clicks"),
    State("test-form", "children"),
    # todo this function should also listen to changes in the variables inputs
)
def update_outputs(selected_model, form, form_content):

    # print(f"{form_content=}")

    # todo we should extract the input values from the form_content
    # todo we should also check the units
    # todo the following function should be moved outside the code
    def find_dict_with_key_value(d, key, value):
        if isinstance(d, dict):
            if d.get(key) == value:
                return d
            for k, v in d.items():
                result = find_dict_with_key_value(v, key, value)
                if result is not None:
                    return result
        elif isinstance(d, list):
            for item in d:
                result = find_dict_with_key_value(item, key, value)
                if result is not None:
                    return result
        return None

    if selected_model is None:
        return no_update

    results = []
    columns: int = 2
    if selected_model == Models.PMV_EN.name:
        # todo the variables below should not be hardcoded
        columns = 2
        # todo the code below is not great and should be improved
        result_dict = find_dict_with_key_value(
            form_content, "id", ElementsIDs.t_db_input.value
        )
        tdb = result_dict["value"]
        result_dict = find_dict_with_key_value(
            form_content, "id", ElementsIDs.t_r_input.value
        )
        tr = result_dict["value"]
        result_dict = find_dict_with_key_value(
            form_content, "id", ElementsIDs.v_input.value
        )
        v = result_dict["value"]

        r_pmv = pmv_ppd(
            tdb=tdb,
            tr=tr,
            vr=v,
            rh=50,
            met=1.2,
            clo=0.5,
            wme=0,
            limit_inputs=False,
            standard="ISO",
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))

    return (
        dmc.SimpleGrid(
            cols=columns,
            spacing="xs",
            verticalSpacing="xs",
            children=results,
        ),
    )
