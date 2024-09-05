import dash_mantine_components as dmc

from pythermalcomfort.models import pmv_ppd, adaptive_ashrae, phs
from pythermalcomfort.utilities import v_relative, clo_dynamic, mapping

from utils.get_inputs import get_inputs
from utils.my_config_file import (
    Models,
    UnitSystem,
    UnitConverter,
    ElementsIDs,
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

def display_results(selected_model: str, form_content: dict, units_selection: str):

    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    inputs = get_inputs(selected_model, form_content, units)

    results = []
    columns: int = 2
    if selected_model == Models.PMV_EN.name or selected_model == Models.PMV_ashrae.name:
        columns = 3
        standard = "ISO"
        if selected_model == Models.PMV_ashrae.name:
            standard = "ashrae"

        r_pmv = pmv_ppd(
            tdb=inputs[ElementsIDs.t_db_input.value],
            tr=inputs[ElementsIDs.t_r_input.value],
            vr=v_relative(
                v=inputs[ElementsIDs.v_input.value],
                met=inputs[ElementsIDs.met_input.value],
            ),
            rh=inputs[ElementsIDs.rh_input.value],
            met=inputs[ElementsIDs.met_input.value],
            clo=clo_dynamic(
                clo=inputs[ElementsIDs.clo_input.value],
                met=inputs[ElementsIDs.met_input.value],
            ),
            wme=0,
            limit_inputs=True,
            standard=standard,
        )
        results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv['pmv']}")))
        results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv['ppd']}")))
        comfort_category = mapping(
            r_pmv["pmv"],
            {
                -2.5: "Cold",
                -1.5: "Cool",
                -0.5: "Slightly Cool",
                0.5: "Neutral",
                1.5: "Slightly Warm",
                2.5: "Warm",
                10: "Hot",
            },
        )
        results.append(dmc.Center(dmc.Text(f"Sensation: {comfort_category}")))
    elif selected_model == Models.Adaptive_ASHRAE.name:
        columns = 1

        adaptive = adaptive_ashrae(
            tdb=inputs[ElementsIDs.t_db_input.value],
            tr=inputs[ElementsIDs.t_r_input.value],
            t_running_mean=inputs[ElementsIDs.t_rm_input.value],
            v=inputs[ElementsIDs.v_input.value],
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
