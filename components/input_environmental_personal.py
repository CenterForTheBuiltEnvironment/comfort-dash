from copy import deepcopy

import dash_mantine_components as dmc
from dash import html

from utils.my_config_file import (
    ModelInputsInfo,
    Models,
    convert_units,
    ElementsIDs,
    UnitSystem,
)


def input_environmental_personal(
    selected_model: str = "PMV_ashrae", units: str = UnitSystem.SI.value
):
    inputs = []
    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    values: ModelInputsInfo
    for values in model_inputs:
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

    unit_toggle = dmc.Center(
        dmc.Switch(
            id=ElementsIDs.UNIT_TOGGLE.value,
            label=f"{units} Units",
            checked=units == UnitSystem.IP.value,
        )
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
        id=ElementsIDs.inputs_form.value,
    )
