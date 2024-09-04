import dash_mantine_components as dmc
from dash import html, Input, Output, State, callback
from utils.my_config_file import ModelInputsInfo, Models, convert_units, ElementsIDs, MetabolicRateSelection
import re

def input_environmental_personal(selected_model: str = "PMV_ashrae", units: str = "SI"):
    inputs = []
    model = Models[selected_model].value.inputs
    convert_units(model, units)

    for values in model:
        if values.name == "Metabolic Rate":
            metabolic_input = create_metabolic_rate_input(values)
            inputs.append(metabolic_input)
        else:
            input_field = dmc.NumberInput(
                label=values.name + " (" + values.unit + ")",
                description=f"From {values.min} to {values.max}",
                value=values.value,
                min=values.min,
                max=values.max,
                step=values.step,
                id=values.id,
            )
            inputs.append(input_field)

    unit_toggle = dmc.Switch(
        id=ElementsIDs.UNIT_TOGGLE.value,
        label="IP Units" if units == "IP" else "SI Units",
        checked=units == "IP",
    )

    inputs.append(unit_toggle)

    return html.Form(
        dmc.Paper(
            children=[
                dmc.Grid(
                    children=[
                        dmc.GridCol(dmc.Stack(inputs, gap="xs"), span={"base": 12}),
                    ],
                    gutter="md",
                ),
            ],
            shadow="md",
            p="md",
        ),
        id="test-form", # todo remove this id
    )

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
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)
        except ValueError:
            # skip if the option doesn't have a numeric value
            continue

    # If no close matches, return all options
    if not filtered_options:
        filtered_options = [option.value for option in MetabolicRateSelection]

    return filtered_options, input_value

# def update_metabolic_rate_options(input_value, current_data):
#     if input_value is None or input_value == "":
#         return [], ""
#
#     try:
#         input_number = float(input_value)
#     except ValueError:
#         # If input is not number, return all options
#         return [option.value for option in MetabolicRateSelection], input_value
#
#     filtered_options = []
#     for option in MetabolicRateSelection:
#         # use regex, find the end of the string
#         match = re.search(r':\s*([\d.]+)\s*$', option.value)
#         if match:
#             option_value = float(match.group(1))
#             if abs(option_value - input_number) <1:
#                 filtered_options.append(option.value)
#
#     # if no close matches, return all options
#     if not filtered_options:
#         filtered_options = [option.value for option in MetabolicRateSelection]
#
#     return filtered_options, input_value

@callback(
    Output(ElementsIDs.met_input.value, "value", allow_duplicate=True),
    Input(ElementsIDs.met_input.value, "value"),
    prevent_initial_call=True
)

def update_input_on_selection(selected_value):
    if selected_value in [option.value for option in MetabolicRateSelection]:
        try:
            return selected_value.split(":")[-1].strip()
        except IndexError:
            return "0.8" if "Reclining" in selected_value else selected_value
    return selected_value








