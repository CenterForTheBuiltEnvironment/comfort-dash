from components.drop_down_inline import (
    generate_dropdown_inline,
    generate_dropdown_inputs_inline,
)
from utils.my_config_file import (
    ElementsIDs,
    Models,
    AdaptiveENSpeeds,
    ModelInputsSelectionSpeedASHRAE55,
    HumiditySelection,
    MetabolicRateSelection,
    ClothingSelection,
)
from utils.website_text import TextHome

options: list = []

for model in Models:
    option_dict: dict = {"value": model.name, "label": model.value.name}
    options.append(option_dict)

dd_model = {
    "id": ElementsIDs.MODEL_SELECTION.value,
    "question": TextHome.model_selection.value,
    "options": options,
    "multi": False,
    "default": Models.PMV_ashrae.name,
}


def model_selection():
    return generate_dropdown_inline(dd_model, clearable=False)


adaptive_en_air_speed = {
    "id": ElementsIDs.ADAPTIVE_EN_SPEED_SELECTION.value,
    "question": TextHome.speed_selection.value,
    "options": [
        AdaptiveENSpeeds.s_1.value,
        AdaptiveENSpeeds.s_2.value,
        AdaptiveENSpeeds.S_3.value,
        AdaptiveENSpeeds.s_4.value,
    ],
    "multi": False,
    "default": AdaptiveENSpeeds.s_2.value,
}

pmv_en_humidity_selection = {
    "id": ElementsIDs.HUMIDITY_SELECTION.value,
    "question": "",
    "options": [
        HumiditySelection.h_1.value,
        HumiditySelection.h_2.value,
        HumiditySelection.h_3.value,
        HumiditySelection.h_4.value,
        HumiditySelection.h_5.value,
    ],
    "multi": False,
    "default": HumiditySelection.h_1.value,
}

pmv_en_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.h_3.value,
        MetabolicRateSelection.h_4.value,
        MetabolicRateSelection.h_5.value,
        MetabolicRateSelection.h_6.value,
        MetabolicRateSelection.h_7.value,
        MetabolicRateSelection.h_8.value,
        MetabolicRateSelection.h_9.value,
        MetabolicRateSelection.h_10.value,
        MetabolicRateSelection.h_11.value,
        MetabolicRateSelection.h_12.value,
        MetabolicRateSelection.h_13.value,
        MetabolicRateSelection.h_14.value,
        MetabolicRateSelection.h_15.value,
        MetabolicRateSelection.h_16.value,
        MetabolicRateSelection.h_17.value,
        MetabolicRateSelection.h_18.value,
        MetabolicRateSelection.h_19.value,
        MetabolicRateSelection.h_20.value,
        MetabolicRateSelection.h_21.value,
        MetabolicRateSelection.h_22.value,
        MetabolicRateSelection.h_23.value,
        MetabolicRateSelection.h_24.value,
        MetabolicRateSelection.h_25.value,
        MetabolicRateSelection.h_26.value,
        MetabolicRateSelection.h_27.value,
        MetabolicRateSelection.h_28.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

pmv_en_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.c_1.value,
        ClothingSelection.c_2.value,
        ClothingSelection.c_3.value,
        ClothingSelection.c_4.value,
        ClothingSelection.c_5.value,
        ClothingSelection.c_6.value,
        ClothingSelection.c_7.value,
        ClothingSelection.c_8.value,
        ClothingSelection.c_9.value,
    ],
    "multi": False,
    "default": ClothingSelection.c_1.value,
}

fans_and_heat_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.h_3.value,
        MetabolicRateSelection.h_4.value,
        MetabolicRateSelection.h_5.value,
        MetabolicRateSelection.h_6.value,
        MetabolicRateSelection.h_7.value,
        MetabolicRateSelection.h_8.value,
        MetabolicRateSelection.h_9.value,
        MetabolicRateSelection.h_10.value,
        MetabolicRateSelection.h_11.value,
        MetabolicRateSelection.h_12.value,
        MetabolicRateSelection.h_13.value,
        MetabolicRateSelection.h_14.value,
        MetabolicRateSelection.h_15.value,
        MetabolicRateSelection.h_16.value,
        MetabolicRateSelection.h_17.value,
        MetabolicRateSelection.h_18.value,
        MetabolicRateSelection.h_19.value,
        MetabolicRateSelection.h_20.value,
        MetabolicRateSelection.h_21.value,
        MetabolicRateSelection.h_22.value,
        MetabolicRateSelection.h_23.value,
        MetabolicRateSelection.h_24.value,
        MetabolicRateSelection.h_25.value,
        MetabolicRateSelection.h_26.value,
        MetabolicRateSelection.h_27.value,
        MetabolicRateSelection.h_28.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

fans_and_heat_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.c_1.value,
        ClothingSelection.c_2.value,
        ClothingSelection.c_3.value,
        ClothingSelection.c_4.value,
        ClothingSelection.c_5.value,
        ClothingSelection.c_6.value,
        ClothingSelection.c_7.value,
        ClothingSelection.c_8.value,
        ClothingSelection.c_9.value,
    ],
    "multi": False,
    "default": ClothingSelection.c_1.value,
}

phs_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.h_3.value,
        MetabolicRateSelection.h_4.value,
        MetabolicRateSelection.h_5.value,
        MetabolicRateSelection.h_6.value,
        MetabolicRateSelection.h_7.value,
        MetabolicRateSelection.h_8.value,
        MetabolicRateSelection.h_9.value,
        MetabolicRateSelection.h_10.value,
        MetabolicRateSelection.h_11.value,
        MetabolicRateSelection.h_12.value,
        MetabolicRateSelection.h_13.value,
        MetabolicRateSelection.h_14.value,
        MetabolicRateSelection.h_15.value,
        MetabolicRateSelection.h_16.value,
        MetabolicRateSelection.h_17.value,
        MetabolicRateSelection.h_18.value,
        MetabolicRateSelection.h_19.value,
        MetabolicRateSelection.h_20.value,
        MetabolicRateSelection.h_21.value,
        MetabolicRateSelection.h_22.value,
        MetabolicRateSelection.h_23.value,
        MetabolicRateSelection.h_24.value,
        MetabolicRateSelection.h_25.value,
        MetabolicRateSelection.h_26.value,
        MetabolicRateSelection.h_27.value,
        MetabolicRateSelection.h_28.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

phs_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.c_1.value,
        ClothingSelection.c_2.value,
        ClothingSelection.c_3.value,
        ClothingSelection.c_4.value,
        ClothingSelection.c_5.value,
        ClothingSelection.c_6.value,
        ClothingSelection.c_7.value,
        ClothingSelection.c_8.value,
        ClothingSelection.c_9.value,
    ],
    "multi": False,
    "default": ClothingSelection.c_1.value,
}

pmv_ashrae_speed_selection = {
    "id": ElementsIDs.PMV_ASHRAE_SPEED_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionSpeedASHRAE55.s_1.value,
        ModelInputsSelectionSpeedASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionSpeedASHRAE55.s_1.value,
}

pmv_ashrae_humidity_selection = {
    "id": ElementsIDs.HUMIDITY_SELECTION.value,
    "question": "",
    "options": [
        HumiditySelection.h_1.value,
        HumiditySelection.h_2.value,
        HumiditySelection.h_3.value,
        HumiditySelection.h_4.value,
        HumiditySelection.h_5.value,
    ],
    "multi": False,
    "default": HumiditySelection.h_1.value,
}

pmv_ashrae_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.h_3.value,
        MetabolicRateSelection.h_4.value,
        MetabolicRateSelection.h_5.value,
        MetabolicRateSelection.h_6.value,
        MetabolicRateSelection.h_7.value,
        MetabolicRateSelection.h_8.value,
        MetabolicRateSelection.h_9.value,
        MetabolicRateSelection.h_10.value,
        MetabolicRateSelection.h_11.value,
        MetabolicRateSelection.h_12.value,
        MetabolicRateSelection.h_13.value,
        MetabolicRateSelection.h_14.value,
        MetabolicRateSelection.h_15.value,
        MetabolicRateSelection.h_16.value,
        MetabolicRateSelection.h_17.value,
        MetabolicRateSelection.h_18.value,
        MetabolicRateSelection.h_19.value,
        MetabolicRateSelection.h_20.value,
        MetabolicRateSelection.h_21.value,
        MetabolicRateSelection.h_22.value,
        MetabolicRateSelection.h_23.value,
        MetabolicRateSelection.h_24.value,
        MetabolicRateSelection.h_25.value,
        MetabolicRateSelection.h_26.value,
        MetabolicRateSelection.h_27.value,
        MetabolicRateSelection.h_28.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

pmv_ashare_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.c_1.value,
        ClothingSelection.c_2.value,
        ClothingSelection.c_3.value,
        ClothingSelection.c_4.value,
        ClothingSelection.c_5.value,
        ClothingSelection.c_6.value,
        ClothingSelection.c_7.value,
        ClothingSelection.c_8.value,
        ClothingSelection.c_9.value,
    ],
    "multi": False,
    "default": ClothingSelection.c_1.value,
}


def En16798_air_speed_selection():
    return generate_dropdown_inputs_inline(adaptive_en_air_speed, clearable=False)


def En16798_relative_humidity_selection():
    return generate_dropdown_inputs_inline(pmv_en_humidity_selection, clearable=False)


def En16798_relative_metabolic_selection():
    return generate_dropdown_inputs_inline(pmv_en_metabolic_selection, clearable=False)


def En16798_relative_clothing_selection():
    return generate_dropdown_inputs_inline(pmv_en_clothing_selection, clearable=False)


def Fans_heat_metabolic_selection():
    return generate_dropdown_inputs_inline(
        fans_and_heat_metabolic_selection, clearable=False
    )


def Fans_heat_clothing_selection():
    return generate_dropdown_inputs_inline(
        fans_and_heat_clothing_selection, clearable=False
    )


def Phs_metabolic_selection():
    return generate_dropdown_inputs_inline(
        fans_and_heat_metabolic_selection, clearable=False
    )


def Phs_clothing_selection():
    return generate_dropdown_inputs_inline(
        fans_and_heat_clothing_selection, clearable=False
    )


def ashrae_speed_selection():
    return generate_dropdown_inputs_inline(pmv_ashrae_speed_selection, clearable=False)


def ashrae_humidity_selection():
    return generate_dropdown_inputs_inline(
        pmv_ashrae_humidity_selection, clearable=False
    )


def ashrae_metabolic_selection():
    return generate_dropdown_inputs_inline(
        pmv_ashrae_metabolic_selection, clearable=False
    )


def ashare_clothing_selection():
    return generate_dropdown_inputs_inline(
        pmv_ashare_clothing_selection, clearable=False
    )
