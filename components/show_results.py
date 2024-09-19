import dash_mantine_components as dmc
from pythermalcomfort.models import pmv_ppd, adaptive_ashrae
from pythermalcomfort.utilities import v_relative, clo_dynamic, mapping

from utils.get_inputs import get_inputs
from utils.my_config_file import (
    Models,
    UnitSystem,
    UnitConverter,
    ElementsIDs,
    Functionalities,
    CompareInputColor,
)


def display_results(inputs: dict):
    selected_model: str = inputs[ElementsIDs.MODEL_SELECTION.value]
    units: str = inputs[ElementsIDs.UNIT_TOGGLE.value]

    results = []
    # todo add unit detect if IP inputs and conver into SI calculation
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

        # todo add unit detect if IP inputs and conver into SI calculation
        if (
            inputs[ElementsIDs.functionality_selection.value]
            == Functionalities.Compare.value
            and selected_model == Models.PMV_ashrae.name
        ):
            r_pmv_input2 = pmv_ppd(
                tdb=inputs[ElementsIDs.t_db_input_input2.value],
                tr=inputs[ElementsIDs.t_r_input_input2.value],
                vr=v_relative(
                    v=inputs[ElementsIDs.v_input_input2.value],
                    met=inputs[ElementsIDs.met_input_input2.value],
                ),
                rh=inputs[ElementsIDs.rh_input_input2.value],
                met=inputs[ElementsIDs.met_input_input2.value],
                clo=clo_dynamic(
                    clo=inputs[ElementsIDs.clo_input_input2.value],
                    met=inputs[ElementsIDs.met_input_input2.value],
                ),
                wme=0,
                limit_inputs=True,
                standard=standard,
            )
            results.append(dmc.Center(dmc.Text(f"PMV: {r_pmv_input2['pmv']}")))
            results.append(dmc.Center(dmc.Text(f"PPD: {r_pmv_input2['ppd']}")))
            comfort_category = mapping(
                r_pmv_input2["pmv"],
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

            # Modify the color
            for i in range(len(results)):
                if i < 3:
                    results[i].children.c = CompareInputColor.InputColor1.value
                else:
                    results[i].children.c = CompareInputColor.InputColor2.value

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
    return (
        dmc.SimpleGrid(
            cols=columns,
            spacing="xs",
            verticalSpacing="xs",
            children=results,
        ),
    )
