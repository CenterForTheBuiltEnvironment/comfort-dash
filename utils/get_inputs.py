from copy import deepcopy

from dash import no_update
from utils.my_config_file import (
    Models,
    UnitSystem,
    convert_units,
    ElementsIDs,
    Functionalities,
)


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


def extract_float(value):
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            parts = value.split(":")
            if len(parts) > 1:
                return float(parts[-1].strip().split()[0])
            else:
                return float(value.strip().split()[0])
        except (ValueError, IndexError):
            return None
    return None


def get_inputs(
    selected_model: str, form_content: dict, units: str, functionality_selection: str
):
    if selected_model is None:
        return no_update

    list_model_inputs = list(Models[selected_model].value.inputs)

    if functionality_selection == Functionalities.Compare.value and selected_model in [
        Models.PMV_ashrae.name
    ]:
        list_model_inputs2 = list(Models[selected_model].value.inputs2)
        combined_model_inputs = list_model_inputs + list_model_inputs2
    else:
        combined_model_inputs = list_model_inputs

    # updating the values of the model inputs with the values from the form
    for model_input in combined_model_inputs:
        input_dict = find_dict_with_key_value(form_content, "id", model_input.id)

        if input_dict and "value" in input_dict:
            original_value = input_dict["value"]
            converted_value = extract_float(str(original_value))

            if converted_value is not None:
                model_input.value = converted_value

    # converting the units if necessary
    if units == UnitSystem.IP.value:
        combined_model_inputs = convert_units(
            combined_model_inputs, UnitSystem.IP.value
        )
    elif units == UnitSystem.SI.value:
        combined_model_inputs = convert_units(
            combined_model_inputs, UnitSystem.SI.value
        )

    inputs = {}
    # creat model_inputs_dict to store default value,over range use default
    model_inputs_dict = {
        input.id: input for input in Models[selected_model].value.inputs
    }
    for model_input in combined_model_inputs:
        if model_input.min <= model_input.value <= model_input.max:
            inputs[model_input.id] = model_input.value
        elif model_input.value > model_input.max:
            inputs[model_input.id] = model_input.max
        elif model_input.value < model_input.min:
            inputs[model_input.id] = model_input.min
        else:
            inputs[model_input.id] = model_input.value

    return inputs
