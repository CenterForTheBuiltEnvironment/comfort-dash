from copy import deepcopy

from dash import no_update

from utils.my_config_file import Models, UnitSystem, convert_units, ElementsIDs

'''
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
'''

def get_inputs(selected_model: str, form_content: dict, units: str):

    if selected_model is None:
        return no_update

    # creating a copy of the model inputs
    list_model_inputs = deepcopy(Models[selected_model].value.inputs)
    
    # Update input values ​​to map dynamic IDs to ElementsIDs
    for model_input in list_model_inputs:
        found_input = form_content.get(model_input.id)
        model_input.value = found_input["value"]
    
    # converting the units if necessary
    if units == UnitSystem.IP.value:
        list_model_inputs = convert_units(list_model_inputs, UnitSystem.SI.value)

    inputs = {}
    for model_input in list_model_inputs:
        inputs[model_input.id] = model_input.value
    
    return inputs
