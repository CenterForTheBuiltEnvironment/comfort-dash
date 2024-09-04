import dash
import dash_mantine_components as dmc
from copy import deepcopy

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
    UnitSystem,
    convert_units,
)
from dash import html, dcc, callback, Output, Input, no_update, State
from pythermalcomfort.models import pmv_ppd, adaptive_ashrae

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
def update_inputs(selected_model, units_selection):
    if selected_model is None:
        return no_update
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    return input_environmental_personal(selected_model, units)


@callback(
    Output(ElementsIDs.RESULTS_SECTION.value, "children"),
    Input(dd_model["id"], "value"),
    Input("test-form", "n_clicks"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
    State("test-form", "children"),
    # todo this function should also listen to changes in the variables inputs
)
def update_outputs(selected_model, form, units_selection: str, form_content: dict):

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

    # creating a copy of the model inputs
    list_model_inputs = deepcopy(Models[selected_model].value.inputs)

    # updating the values of the model inputs with the values from the form
    for model_input in list_model_inputs:
        model_input.value = find_dict_with_key_value(
            form_content, "id", model_input.id
        )["value"]

    # converting the units if necessary
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    if units == UnitSystem.IP.value:
        list_model_inputs = convert_units(list_model_inputs, UnitSystem.SI.value)

    results = []
    columns: int = 2
    if selected_model == Models.PMV_EN.name:
        columns = 2

        # todo I do not like we are unpacking the values from the list using position, we should use the key
        r_pmv = pmv_ppd(
            tdb=list_model_inputs[0].value,
            tr=list_model_inputs[1].value,
            vr=list_model_inputs[2].value,
            rh=list_model_inputs[3].value,
            met=list_model_inputs[4].value,
            clo=list_model_inputs[5].value,
            wme=0,
            limit_inputs=False,
            standard="ISO",
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))
    elif selected_model == Models.PMV_ashrae.name:
        columns = 2

        # todo I do not like we are unpacking the values from the list using position, we should use the key
        r_pmv = pmv_ppd(
            tdb=list_model_inputs[0].value,
            tr=list_model_inputs[1].value,
            vr=list_model_inputs[2].value,
            rh=list_model_inputs[3].value,
            met=list_model_inputs[4].value,
            clo=list_model_inputs[5].value,
            wme=0,
            limit_inputs=False,
            standard="ashrae",
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))
    elif selected_model == Models.Adaptive_ASHRAE.name:
        columns = 1

        # todo I do not like we are unpacking the values from the list using position, we should use the key
        adaptive = adaptive_ashrae(
            tdb=list_model_inputs[0].value,
            tr=list_model_inputs[1].value,
            t_running_mean=list_model_inputs[2].value,
            v=list_model_inputs[3].value,
        )
        results.append(dmc.Center(dmc.Text(f"Comfort temperature: {adaptive.tmp_cmf}")))
        results.append(
            dmc.Center(
                dmc.Text(
                    f"Comfort range for 80% occupants: {adaptive.tmp_cmf_80_low} - {adaptive.tmp_cmf_80_up}"
                )
            )
        )
        results.append(
            dmc.Center(
                dmc.Text(
                    f"Comfort range for 90% occupants: {adaptive.tmp_cmf_90_low} - {adaptive.tmp_cmf_90_up}"
                )
            )
        )

    return (
        dmc.SimpleGrid(
            cols=columns,
            spacing="xs",
            verticalSpacing="xs",
            children=results,
        ),
    )
