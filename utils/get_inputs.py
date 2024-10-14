from copy import deepcopy

from dash import no_update

from utils.my_config_file import Models, UnitSystem, convert_units, ElementsIDs


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
            # Strip leading/trailing whitespace and split by ':' if it exists
            stripped_value = value.strip()
            if ":" in stripped_value:
                stripped_value = stripped_value.split(":")[-1].strip()
            # Split by any non-numeric character to handle different formats
            parts = stripped_value.split()
            # Convert the first part that looks numeric to float
            return float(parts[0])
        except (ValueError, IndexError):
            return None
    return None


def get_inputs(selected_model: str, form_content: dict, units: str):
    if selected_model is None:
        return no_update

    # creating a copy of the model inputs
    list_model_inputs = deepcopy(Models[selected_model].value.inputs)

    # updating the values of the model inputs with the values from the form
    for model_input in list_model_inputs:
        input_dict = find_dict_with_key_value(form_content, "id", model_input.id)

        if input_dict and "value" in input_dict:
            original_value = input_dict["value"]
            converted_value = extract_float(str(original_value))

            if converted_value is not None:
                model_input.value = converted_value

    # converting the units if necessary
    if units == UnitSystem.IP.value:
        list_model_inputs = convert_units(list_model_inputs, UnitSystem.IP.value)
    elif units == UnitSystem.SI.value:
        list_model_inputs = convert_units(list_model_inputs, UnitSystem.SI.value)

    # range checking after unit conversion
    inputs = {}
    model_inputs_dict = {
        input.id: input for input in Models[selected_model].value.inputs
    }
    for model_input in list_model_inputs:
        if model_input.min <= model_input.value <= model_input.max:
            inputs[model_input.id] = model_input.value
        else:
            # change the value to default
            default_value = model_inputs_dict[model_input.id].value
            inputs[model_input.id] = default_value

    return inputs
