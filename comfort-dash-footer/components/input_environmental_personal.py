from utils.my_config_file import (
    ModelInputsAdaptiveAshrae55,
    ModelInputsInfo,
    ModelInputsPmvAshrae55,
    ModelInputsAdaptiveEN16798,
    ModelInputsPmvEN16798,
    MODELS,
)
import dash_mantine_components as dmc
from components.dropdowns import Ash55_air_speed_selection, En16798_air_speed_selection


def input_environmental_personal(selected_model):
    inputs = []

    model_inputs = ModelInputsPmvAshrae55()
    if selected_model == "Adaptive - EN 16798":

        model_inputs = ModelInputsAdaptiveEN16798()
    elif selected_model == "PMV - ASHRAE 55":
        model_inputs = ModelInputsPmvAshrae55()

    elif selected_model == "Adaptive - ASHRAE 55":
        model_inputs = ModelInputsAdaptiveAshrae55()

    elif selected_model == "PMV - EN 16798":
        model_inputs = ModelInputsPmvEN16798()

    for var_name, values in dict(model_inputs).items():
        input_filed = dmc.NumberInput(
            label=values.name,
            description=f"From {values.min} to {values.max}",
            value=values.value,
            min=values.min,
            max=values.max,
            step=values.step,
        )
        inputs.append(input_filed)

    if selected_model == "Adaptive - ASHRAE 55":
        inputs.append(Ash55_air_speed_selection())

    if selected_model == "Adaptive - EN 16798":
        inputs.append(En16798_air_speed_selection())

    return dmc.Paper(
        # children=[dmc.Text("Inputs", mb="xs", fw=700), dmc.GridCol(dmc.Stack(inputs, gap="xs"),span={"base":12,"sm":7}),generate_buttons()],
        children=[dmc.Text("Inputs", mb="xs", fw=700), dmc.GridCol(dmc.Stack(inputs, gap="xs"),span={"base":12,"sm":7})],
        shadow="md",
        p="md",
    )
