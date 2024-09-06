import dash_mantine_components as dmc
from dash import html, callback, Output, Input, State

from utils.my_config_file import (
    ModelInputsInfo,
    Models,
    convert_units,
    ElementsIDs,
    UnitSystem,
    MetabolicRateSelection,
    ClothingSelection,
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


def input_environmental_personal(selected_model: str = "PMV_ashrae", units: str = UnitSystem.SI.value):
    inputs = []
    # create empty collection to keep track of the input field names that have been added
    added_inputs = set()
    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    values: ModelInputsInfo
    for values in model_inputs:
        # Checks whether the current input field name already exists in the collection
        if values.name in added_inputs:
            continue # if already exists, skip the loop to prevent repeated addition

        if values.name == "Metabolic Rate":
            metabolic_input = create_metabolic_rate_input(values)
            inputs.append(metabolic_input)
        elif values.name == "Clothing Level":
            clothing_input = create_clothing_level_input(values)
            inputs.append(clothing_input)
        else:
            input_filed = dmc.NumberInput(
                label=values.name + " (" + values.unit + ")",
                description=f"From {values.min} to {values.max}",
                value=values.value,
                min=values.min,
                max=values.max,
                step=values.step,
                id=values.id,
            )
            inputs.append(input_filed)

        added_inputs.add(values.name)

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


def create_metabolic_rate_input(values: ModelInputsInfo):
    return dmc.Autocomplete(
        id=values.id,
        label=f"{values.name} ({values.unit})",
        placeholder="Enter a value or select an activity",
        data=[],
        value=str(values.value),
        description=f"From {values.min} to {values.max}",
    )

@callback(
    Output(ElementsIDs.met_input.value, "data"),
    Output(ElementsIDs.met_input.value, "value"),
    Input(ElementsIDs.met_input.value, "value"),
    State(ElementsIDs.met_input.value, "data")
)

def update_metabolic_rate_options(input_value, current_data):
    print(input_value)
    if input_value is None or input_value == "":
        return [], ""

    try:
        input_number = float(input_value)
    except ValueError:
        # if input is not a number, return all options
        return [option.value for option in MetabolicRateSelection], input_value

    # filter options based on input value
    filtered_options = []
    for option in MetabolicRateSelection:
        try:
            option_value = float(option.value.split(":")[-1].strip())
            # select the related options
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)
        except ValueError:
            # skip if the option doesn't have a numeric value
            continue

    # If no close matches, return all options
    if not filtered_options:
        filtered_options = [option.value for option in MetabolicRateSelection]

    return filtered_options, input_value

@callback(
    Output(ElementsIDs.met_input.value, "value", allow_duplicate=True),
    Input(ElementsIDs.met_input.value, "value"),
    prevent_initial_call=True
)


def update_input_on_selection(selected_value):
    if selected_value in [option.value for option in MetabolicRateSelection]:
        try:
            return float(selected_value.split(":")[-1].strip().split()[0])
        except IndexError:
            return "0.8" if "Reclining" in selected_value else selected_value
    return selected_value


#---------------------clo
def create_clothing_level_input(values: ModelInputsInfo):
    return dmc.Autocomplete(
        id=values.id,
        label=f"{values.name} ({values.unit})",
        placeholder="Enter a value or select clothing",
        data=[],
        value=str(values.value),
        description=f"From {values.min} to {values.max}",
    )

@callback(
    Output(ElementsIDs.clo_input.value, "data"),
    Output(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.clo_input.value, "value"),
    State(ElementsIDs.clo_input.value, "data")
)

def update_clothing_level_options(input_value, current_data):
    if input_value is None or input_value == "":
        return [], ""
    try:
        input_number = float(input_value)
    except ValueError:
        return [option.value for option in ClothingSelection], input_value

    filtered_options = []
    for option in ClothingSelection:
        try:
            option_value = float(option.value.split(":")[-1].strip().split()[0])
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)
        except ValueError:
            continue

    if not filtered_options:
        filtered_options = [option.value for option in ClothingSelection]
    return filtered_options, input_value


@callback(
    Output(ElementsIDs.clo_input.value, "value", allow_duplicate=True),
    Input(ElementsIDs.clo_input.value, "value"),
    prevent_initial_call=True
)

def update_clothing_input_on_selection(selected_value):
    if selected_value in [option.value for option in ClothingSelection]:
        try:
            return float(selected_value.split(":")[-1].strip().split()[0])
        except IndexError:
            return selected_value
    return selected_value