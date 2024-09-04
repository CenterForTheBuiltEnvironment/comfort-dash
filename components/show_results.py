from copy import deepcopy

import dash_mantine_components as dmc
from dash import no_update
from pythermalcomfort.models import pmv_ppd, adaptive_ashrae

from utils.my_config_file import (
    Models,
    UnitSystem,
    convert_units,
    UnitConverter,
)


def display_results(selected_model: str, form_content: dict, units_selection: str):
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
        if units == UnitSystem.IP.value:
            adaptive.tmp_cmf = round(
                UnitConverter.celsius_to_fahrenheit(adaptive.tmp_cmf), 2
            )
            adaptive.tmp_cmf_80_low = round(
                UnitConverter.celsius_to_fahrenheit(adaptive.tmp_cmf_80_low), 2
            )
            adaptive.tmp_cmf_80_up = round(
                UnitConverter.celsius_to_fahrenheit(adaptive.tmp_cmf_80_up), 2
            )
            adaptive.tmp_cmf_90_low = round(
                UnitConverter.celsius_to_fahrenheit(adaptive.tmp_cmf_90_low), 2
            )
            adaptive.tmp_cmf_90_up = round(
                UnitConverter.celsius_to_fahrenheit(adaptive.tmp_cmf_90_up), 2
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
