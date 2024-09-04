import dash_mantine_components as dmc
from dash import html

from utils.my_config_file import ModelInputsInfo, Models, convert_units, ElementsIDs


def input_environmental_personal(selected_model: str = "PMV_ashrae", units: str = "SI"):
    inputs = []
    model = Models[selected_model].value.inputs
    convert_units(model, units)

    values: ModelInputsInfo
    for values in model:
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
        id="test-form",  # todo remove this id
    )
