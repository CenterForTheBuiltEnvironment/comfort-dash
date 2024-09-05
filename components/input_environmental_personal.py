import dash_mantine_components as dmc
from dash import html, callback, Output, Input, State

from utils.my_config_file import (
    ModelInputsInfo,
    Models,
    convert_units,
    ElementsIDs,
    UnitSystem,
)


def modal_custom_ensemble():
    return dmc.Modal(
        title="Custom Ensemble",
        id="modal-simple",
        zIndex=10000,
        children=[
            dmc.Stack(
                [
                    dmc.Text(
                        "Select all the garments you want to include in the ensemble"
                    ),
                    dmc.MultiSelect(
                        data=[
                            {
                                "group": "Underwear",
                                "items": [
                                    {"value": "React", "label": "React"},
                                    {"value": "Angular", "label": "Angular"},
                                ],
                            },
                            {
                                "group": "Tops",
                                "items": [
                                    # todo change these values
                                    {"value": "Svelte", "label": "Svelte"},
                                    {"value": "Vue", "label": "Vue"},
                                ],
                            },
                            {
                                "group": "Trousers",
                                "items": [
                                    {
                                        "value": "Thin trousers",
                                        "label": "Thin trousers",
                                    },
                                    {
                                        "value": "Thick trousers",
                                        "label": "Thick trousers",
                                    },
                                ],
                            },
                            {
                                "group": "Shoes",
                                "items": [
                                    {"value": "Boots", "label": "Boots"},
                                    {"value": "Flip flops", "label": "Flip flops"},
                                ],
                            },
                        ],
                        styles={"dropdown": {"z-index": "10002"}},
                        # w=400,
                    ),
                    dmc.Group(
                        [
                            # todo when we press submit we should update the clo value in the inputs
                            dmc.Button("Set Clo value", id="modal-submit-button"),
                            dmc.Button(
                                "Close",
                                color="red",
                                variant="outline",
                                id="modal-close-button",
                            ),
                        ],
                        justify="flex-end",
                    ),
                ]
            )
        ],
    )


def input_environmental_personal(
    selected_model: str = "PMV_ashrae", units: str = UnitSystem.SI.value
):
    inputs = []
    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    values: ModelInputsInfo
    for values in model_inputs:
        input_filed = dmc.NumberInput(
            label=values.name + " (" + values.unit + ")",
            description=f"From {values.min} to {values.max}",
            value=values.value,
            min=values.min,
            max=values.max,
            step=values.step,
            id={"type": "dynamic-input", "index": values.id},
        )
        inputs.append(input_filed)

    unit_toggle = dmc.Center(
        dmc.Switch(
            id=ElementsIDs.UNIT_TOGGLE.value,
            label=f"{units} Units",
            checked=units == UnitSystem.IP.value,
        )
    )

    inputs.append(unit_toggle)

    return dmc.Paper(
        children=[
            dmc.Stack(
                [
                    html.Form(
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    dmc.Stack(inputs, gap="xs"), span={"base": 12}
                                ),
                            ],
                            gutter="md",
                        ),
                        id=ElementsIDs.inputs_form.value,
                    ),
                    dmc.Button("Custom Ensemble", id="modal-demo-button"),
                    modal_custom_ensemble(),
                ],
                gap="xs",
            )
        ],
        shadow="md",
        p="md",
    )


@callback(
    Output("modal-simple", "opened"),
    Input("modal-demo-button", "n_clicks"),
    Input("modal-close-button", "n_clicks"),
    Input("modal-submit-button", "n_clicks"),
    State("modal-simple", "opened"),
    prevent_initial_call=True,
)
def modal_demo(nc1, nc2, nc3, opened):
    return not opened
