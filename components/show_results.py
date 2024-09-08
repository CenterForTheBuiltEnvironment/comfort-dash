from copy import deepcopy

import dash_mantine_components as dmc
from dash import no_update
from pythermalcomfort.models import pmv_ppd, adaptive_ashrae, phs

from utils.my_config_file import (
    Models,
    UnitSystem,
    convert_units,
    UnitConverter,
    ElementsIDs,
)
'''
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
def display_results(selected_model: str, form_content: dict, units_selection: str):
    if selected_model is None:
        return no_update

    # creating a copy of the model inputs
    model_inputs_dict = {input.id: input for input in Models[selected_model].value.inputs}

    # updating the values of the model inputs with the values from the form
    for model_input_id, model_input in model_inputs_dict.items():
        found_input = form_content.get(model_input_id)
        model_input.value = found_input["value"]

    # converting the units if necessary
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    if units == UnitSystem.IP.value:
        model_inputs_dict = convert_units(list(model_inputs_dict.values()), UnitSystem.SI.value)

    results = []
    columns: int = 2
    if selected_model == Models.PMV_EN.name:
        columns = 2

        r_pmv = pmv_ppd(
            tdb=model_inputs_dict[ElementsIDs.t_db_input.value].value,
            tr=model_inputs_dict[ElementsIDs.t_r_input.value].value,
            vr=model_inputs_dict[ElementsIDs.v_input.value].value,
            rh=model_inputs_dict[ElementsIDs.rh_input.value].value,
            met=model_inputs_dict[ElementsIDs.met_input.value].value,
            clo=model_inputs_dict[ElementsIDs.clo_input.value].value,
            wme=0,
            limit_inputs=False,
            standard="ISO",
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))
    elif selected_model == Models.PMV_ashrae.name:
        columns = 2

        r_pmv = pmv_ppd(
            tdb=model_inputs_dict[ElementsIDs.t_db_input.value].value,
            tr=model_inputs_dict[ElementsIDs.t_r_input.value].value,
            vr=model_inputs_dict[ElementsIDs.v_input.value].value,
            rh=model_inputs_dict[ElementsIDs.rh_input.value].value,
            met=model_inputs_dict[ElementsIDs.met_input.value].value,
            clo=model_inputs_dict[ElementsIDs.clo_input.value].value,
            wme=0,
            limit_inputs=False,
            standard="ashrae",
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))
    elif selected_model == Models.Adaptive_ASHRAE.name:
        columns = 1

        adaptive = adaptive_ashrae(
            tdb=model_inputs_dict[ElementsIDs.t_db_input.value].value,
            tr=model_inputs_dict[ElementsIDs.t_r_input.value].value,
            t_running_mean=model_inputs_dict[ElementsIDs.t_rm_input.value].value,
            v=model_inputs_dict[ElementsIDs.v_input.value].value,
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
    elif selected_model == Models.PHS.name:
        columns = 1

        r_phs = phs(
            tdb=inputs[ElementsIDs.t_db_input.value],
            tr=inputs[ElementsIDs.t_r_input.value],
            v=inputs[ElementsIDs.v_input.value],
            rh=inputs[ElementsIDs.rh_input.value],
            met=inputs[ElementsIDs.met_input.value],
            clo=inputs[ElementsIDs.clo_input.value],
            posture=inputs[ElementsIDs.posture_input.value],
            wme=0,
            limit_inputs=False,
        )
        results.append(dmc.Center(dmc.Text(f"Maximum allowable exposure time within which the physiological strain is acceptable (no physical damage is to be expected) calculated as a function of:")))
        results.append(dmc.Center(dmc.Text(f"max rectal temperature = {r_phs['t_re']} °C")))
        results.append(dmc.Center(dmc.Text(f"water loss of 5% of the body mass for 95% of the population = {r_phs['d_lim_loss_95']} min")))
        results.append(dmc.Center(dmc.Text(f"water loss of 7.5% of the body mass for an average person = {r_phs['d_lim_loss_50']} min")))

    return (
        dmc.SimpleGrid(
            cols=columns,
            spacing="xs",
            verticalSpacing="xs",
            children=results,
        ),
    )
