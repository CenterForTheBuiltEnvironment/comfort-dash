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
            return float(value.split(":")[-1].strip().split()[0])
        except ValueError:
            return None
    return None


# def get_inputs(selected_model: str, form_content: dict, units: str, function_selection: str):
#     if selected_model is None:
#         return no_update

#     # creating a copy of the model inputs
#     list_model_inputs = deepcopy(Models[selected_model].value.inputs)

#     # converting the units if necessary
#     if units == UnitSystem.IP.value:
#         list_model_inputs = convert_units(list_model_inputs, UnitSystem.SI.value)

#     # updating the values of the model inputs with the values from the form
#     inputs = {}
#     for model_input in list_model_inputs:
#         default_value = model_input.value
#         input_dict = find_dict_with_key_value(form_content, "id", model_input.id)

#         if input_dict and "value" in input_dict:
#             original_value = input_dict["value"]
#             converted_value = extract_float(str(original_value))

#             if (
#                 converted_value is not None
#                 and model_input.min <= converted_value <= model_input.max
#             ):
#                 inputs[model_input.id] = converted_value
#             else:
#                 inputs[model_input.id] = default_value
#         else:
#             inputs[model_input.id] = default_value
#     return inputs


# def get_inputs(selected_model: str, form_content: dict, units: str, functionality_selection: str):
#     if selected_model is None:
#         return no_update

#     # Creating a copy of the model inputs
#     list_model_inputs = deepcopy(Models[selected_model].value.inputs)

#     # Check if in Compare mode and concatenate inputs2
#     if functionality_selection == Functionalities.Compare.value:
#         list_model_inputs2 = deepcopy(Models[selected_model].value.inputs2)
#         # Combine inputs and inputs2 into a single list
#         combined_model_inputs = list_model_inputs + list_model_inputs2
#     else:
#         combined_model_inputs = list_model_inputs

#     # Converting the units if necessary
#     if units == UnitSystem.IP.value:
#         combined_model_inputs = convert_units(combined_model_inputs, UnitSystem.SI.value)

#     # Processing the combined list of inputs
#     inputs = {}
#     for model_input in combined_model_inputs:
#         default_value = model_input.value
#         input_dict = find_dict_with_key_value(form_content, "id", model_input.id)

#         if input_dict and "value" in input_dict:
#             original_value = input_dict["value"]
#             converted_value = extract_float(str(original_value))

#             if (
#                 converted_value is not None
#                 and model_input.min <= converted_value <= model_input.max
#             ):
#                 inputs[model_input.id] = converted_value
#             else:
#                 inputs[model_input.id] = default_value
#         else:
#             inputs[model_input.id] = default_value

#     return inputs


def get_inputs(
    selected_model: str, form_content: dict, units: str, functionality_selection: str
):
    if selected_model is None:
        return no_update

    # Creating a copy of the model inputs
    list_model_inputs = deepcopy(Models[selected_model].value.inputs)

    # Check if in Compare mode and concatenate inputs2
    if functionality_selection == Functionalities.Compare.value and selected_model in [
        Models.PMV_ashrae.name
    ]:
        list_model_inputs2 = deepcopy(Models[selected_model].value.inputs2)
        # Combine inputs and inputs2 into a single list
        combined_model_inputs = list_model_inputs + list_model_inputs2
    else:
        combined_model_inputs = list_model_inputs

    # Converting the units if necessary
    if units == UnitSystem.IP.value:
        combined_model_inputs = convert_units(
            combined_model_inputs, UnitSystem.SI.value
        )

    # Processing the combined list of inputs
    inputs = {}
    for model_input in combined_model_inputs:
        default_value = model_input.value
        input_id = model_input.id
        input_dict = find_dict_with_key_value(form_content, "id", input_id)

        if input_dict and "value" in input_dict:
            original_value = input_dict["value"]
            converted_value = extract_float(str(original_value))

            if (
                converted_value is not None
                and model_input.min <= converted_value <= model_input.max
            ):
                inputs[input_id] = converted_value
            else:
                inputs[input_id] = default_value
        else:
            inputs[input_id] = default_value

    # print(f"Final inputs collected: {inputs}")
    return inputs
