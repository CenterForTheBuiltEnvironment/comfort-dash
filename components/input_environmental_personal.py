from utils.my_config_file import ModelInputs, ModelInputsInfo
import dash_mantine_components as dmc
from dataclasses import fields


def input_environmental_personal():
    inputs = []
    for var_name, values in dict(ModelInputs()).items():
        input_filed = dmc.NumberInput(
            label=values.name,
            description=f"From {values.min} to {values.max}",
            value=values.value,
            min=values.min,
            max=values.max,
            step=values.step,
        )
        inputs.append(input_filed)

    return dmc.Stack(inputs, gap="xs")
