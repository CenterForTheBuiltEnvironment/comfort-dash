from utils.my_config_file import (
    ModelInputsAdaptiveAshrae55,
    ModelInputsInfo,
    ModelInputsPmvAshrae55,
    ModelInputsAdaptiveEN16798,
    ModelInputsPmvEN16798,
    ModelInputsSelectionOperativeTemperaturePmvEN16798,
    ModelInputsFANSHEAT,
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
    ModelInputsSelectionSpeedASHRAE55List_selection,
    ModelInputsSelectionhumidityASHRAE55List_selection,
    ModelInputsSelectionMetabolicASHRAE55List_selection,
    ModelInputsSelectionClothingASHRAE55List_selection,
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
        model_inputs = ModelInputsFANSHEAT()

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

    #Speed selection
    inputs_left_and_right = []
    if selected_model == MODELS.Adaptive_ashrae.value:
        inputs_left_and_right.append(Ash55_air_speed_selection())

    if selected_model == MODELS.Adaptive_EN.value:
        inputs_left_and_right.append(En16798_air_speed_selection())

    #Inputs right selection
    inputs_right = []

    if selected_model == MODELS.PMV_EN.value:
        inputs_right.append(dmc.Space(h=40))
        inputs_right.append(
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=False,
                style={"margin-left": "25px"},
            )
        )
        inputs_right.append(dmc.Space(h=243))
        inputs_right.append(En16798_relative_humidity_selection())
        inputs_right.append(dmc.Space(h=26))
        inputs_right.append(En16798_relative_metabolic_selection())
        inputs_right.append(dmc.Space(h=45))
        inputs_right.append(En16798_relative_clothing_selection())

    elif selected_model == MODELS.Adaptive_EN.value:
        inputs_right.append(dmc.Space(h=40)),
        inputs_right.append(
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=False,
                style={"margin-left": "25px"},
            )
        )

    elif selected_model == MODELS.Adaptive_ashrae.value:
        inputs_right.append(dmc.Space(h=40)),
        inputs_right.append(
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=True,
                style={"margin-left": "25px"},
            )
        )

    elif selected_model == MODELS.Fans_heat.value:
        inputs_right.append(dmc.Space(h=125)),
        inputs_right.append(Fans_heat_metabolic_selection()),
        inputs_right.append(dmc.Space(h=26)),
        inputs_right.append(Fans_heat_clothing_selection()),

    elif selected_model == MODELS.Phs.value:
        inputs_right.append(dmc.Space(h=415)),
        inputs_right.append(Phs_metabolic_selection()),
        inputs_right.append(dmc.Space(h=25)),
        inputs_right.append(Phs_clothing_selection()),

    # PMV - ASHARE right button
    else:
        inputs_right.append(dmc.Space(h=40)),
        inputs_right.append(
            dmc.Checkbox(
                label=ModelInputsSelectionOperativeTemperaturePmvEN16798.o_1.value,
                checked=True,
                style={"margin-left": "25px"},
            )
        )
        inputs_right.append(dmc.Space(h=134)),
        inputs_right.append(ModelInputsSelectionSpeedASHRAE55List_selection())
        inputs_right.append(dmc.Space(h=45)),
        inputs_right.append(ModelInputsSelectionhumidityASHRAE55List_selection())
        inputs_right.append(dmc.Space(h=26)),
        inputs_right.append(ModelInputsSelectionMetabolicASHRAE55List_selection())
        inputs_right.append(dmc.Space(h=27)),
        inputs_right.append(ModelInputsSelectionClothingASHRAE55List_selection())

    return dmc.Paper(
        children=[
            dmc.Text("Inputs", mb="xs", fw=700),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Stack(inputs, gap="xs"), span={"base": 12, "sm": 5}
                    ),
                    dmc.GridCol(
                        dmc.Stack(inputs_right, gap="xs"), span={"base": 12, "sm": 7}
                    ),
                    dmc.GridCol(
                        dmc.Stack(inputs_left_and_right, gap="xs"),
                        span={"base": 12, "sm": 12},
                    ),
                ],
                gutter="md",
            ),
        ],
        shadow="md",
        p="md",
    )
