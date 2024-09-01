from utils.my_config_file import (
    ModelInputsAdaptiveAshrae55,
    ModelInputsInfo,
    ModelInputsPmvAshrae55,
    ModelInputsAdaptiveEN16798,
    ModelInputsPmvEN16798,
    ModelInputsSelectionOperativeTemperaturePmvEN16798,
    ModelInputsFansHeat,
    ModelInputsPhs,
    MODELS,
)
import dash_mantine_components as dmc
from components.dropdowns import (
    Ash55_air_speed_selection,
    En16798_air_speed_selection,
    En16798_relative_humidity_selection,
    En16798_relative_metabolic_selection,
    En16798_relative_clothing_selection,
    Fans_heat_metabolic_selection,
    Fans_heat_clothing_selection,
    Phs_metabolic_selection,
    Phs_clothing_selection,
    ashrae_speed_selection,
    ashrae_humidity_selection,
    ashrae_metabolic_selection,
    ashare_clothing_selection,
)


def input_environmental_personal(selected_model):
    inputs = []

    model_inputs = ModelInputsPmvAshrae55()
    if selected_model == MODELS.Adaptive_EN.value:

        model_inputs = ModelInputsAdaptiveEN16798()
    elif selected_model == MODELS.PMV_ashrae.value:
        model_inputs = ModelInputsPmvAshrae55()

    elif selected_model == MODELS.Adaptive_ashrae.value:
        model_inputs = ModelInputsAdaptiveAshrae55()

    elif selected_model == MODELS.PMV_EN.value:
        model_inputs = ModelInputsPmvEN16798()

    elif selected_model == MODELS.Fans_heat.value:
        model_inputs = ModelInputsFansHeat()

    elif selected_model == MODELS.Phs.value:
        model_inputs = ModelInputsPhs()

    else:
        model_inputs = ModelInputsPmvAshrae55()

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

    # Speed selection
    inputs_left_and_right = []
    if selected_model == MODELS.Adaptive_ashrae.value:
        inputs_left_and_right.append(Ash55_air_speed_selection())

    if selected_model == MODELS.Adaptive_EN.value:
        inputs_left_and_right.append(En16798_air_speed_selection())

    # Inputs right selection
    inputs_right = []

    if selected_model == MODELS.PMV_EN.value:
        inputs_right = [
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=False,
            ),
            En16798_relative_humidity_selection(),
            En16798_relative_metabolic_selection(),
            En16798_relative_clothing_selection(),
        ]
    elif selected_model == MODELS.Adaptive_EN.value:
        inputs_right = [
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=False,
            ),
        ]
    elif selected_model == MODELS.Adaptive_ashrae.value:
        inputs_right = [
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=True,
            ),
        ]
    elif selected_model == MODELS.Fans_heat.value:
        inputs_right = [
            Fans_heat_metabolic_selection(),
            Fans_heat_clothing_selection(),
        ]
    elif selected_model == MODELS.Phs.value:
        inputs_right = [
            Phs_metabolic_selection(),
            Phs_clothing_selection(),
        ]
    else:  # PMV - ASHRAE
        inputs_right = [
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=True,
            ),
            ashrae_speed_selection(),
            ashrae_humidity_selection(),
            ashrae_metabolic_selection(),
            ashare_clothing_selection(),
        ]

    # Pair right with left
    paired_inputs = []
    for i in range(max(len(inputs), len(inputs_right))):
        input_item = inputs[i] if i < len(inputs) else None
        selection_item = inputs_right[i] if i < len(inputs_right) else None
        paired_inputs.append((input_item, selection_item))

    return dmc.Paper(
        children=[
            dmc.Text("Inputs", mb="xs", fw=700),
            dmc.Stack(
                children=[
                    dmc.Grid(
                        children=[
                            dmc.GridCol(input_item, span={"base": 12, "sm": 6}, className="input-field"),
                            dmc.GridCol(
                                dmc.Box(selection_item, className="selection-wrapper") if selection_item else None,
                                span={"base": 12, "sm": 6},
                                className="selection-field"
                            ),
                        ],
                        gutter="xs",
                        align="flex-end",
                        className="input-selection-pair",
                    ) for input_item, selection_item in paired_inputs
                ],
                gap="md",
            ),
        ],
        shadow="md",
        p="md",
    )