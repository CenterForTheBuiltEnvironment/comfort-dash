from scipy._lib.cobyqa.models import Models

from components.drop_down_inline import generate_dropdown_inline, generate_dropdown_inputs_inline
from utils.my_config_file import (
    ElementsIDs,
    MODELS,
    CHARTS,
    AdaptiveAshraeSpeeds,
    AdaptiveENSpeeds,
    ModelInputsSelectionHumidityPmvEN16798,
    ModelInputsSelectionMetablicRatePmvEN16798,
    ModelInputsSelectionClothingPmvEN16798
)
from utils.website_text import TextHome

dd_model = {
    "id": ElementsIDs.MODEL_SELECTION.value,
    "question": TextHome.model_selection.value,
    "options": [
        MODELS.PMV_ashrae.value,
        MODELS.Adaptive_ashrae.value,
        MODELS.PMV_EN.value,
        MODELS.Adaptive_EN.value,
    ],
    "multi": False,
    "default": MODELS.PMV_ashrae.value,
}


def model_selection():
    return generate_dropdown_inline(dd_model, clearable=False)


ashare_chart = {
    "id": ElementsIDs.CHART_SELECTION.value,
    "question": TextHome.chart_selection.value,
    "options": [
        CHARTS.psychrometric.value,
        CHARTS.Psychrometric_operative.value,
        CHARTS.Relative_humidity.value,
        CHARTS.Air_speed.value,
        CHARTS.Thermal_heat.value,
        CHARTS.Set_outputs.value,
    ],
    "multi": False,
    "default": CHARTS.Psychrometric_operative.value,
}

pmv_en_chart = {
    "id": ElementsIDs.CHART_SELECTION.value,
    "question": TextHome.chart_selection.value,
    "options": [
        CHARTS.psychrometric.value,
        CHARTS.Psychrometric_operative.value,
        CHARTS.Relative_humidity.value,
    ],
    "multi": False,
    "default": CHARTS.psychrometric.value,
}


def chart_selection(selected_model):
    chart_inputs = ashare_chart

    if selected_model == MODELS.PMV_ashrae.value:
        chart_inputs = ashare_chart
    elif selected_model == MODELS.Adaptive_ashrae.value:
        return
    elif selected_model == MODELS.Adaptive_EN.value:
        return
    elif selected_model == MODELS.PMV_EN.value:
        chart_inputs = pmv_en_chart

    return generate_dropdown_inline(chart_inputs, clearable=False)


adaptive_ashare_air_speed = {
    "id": ElementsIDs.SPEED_SELECTION.value,
    "question": TextHome.speed_selection.value,
    "options": [
        AdaptiveAshraeSpeeds.s_1.value,
        AdaptiveAshraeSpeeds.s_2.value,
        AdaptiveAshraeSpeeds.S_3.value,
        AdaptiveAshraeSpeeds.s_4.value,
    ],
    "multi": False,
    "default": AdaptiveAshraeSpeeds.s_1.value,
}

adaptive_en_air_speed = {
    "id": ElementsIDs.SPEED_SELECTION.value,
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
        ModelInputsSelectionHumidityPmvEN16798.h_1.value,
        ModelInputsSelectionHumidityPmvEN16798.h_2.value,
        ModelInputsSelectionHumidityPmvEN16798.h_3.value,
        ModelInputsSelectionHumidityPmvEN16798.h_4.value,
        ModelInputsSelectionHumidityPmvEN16798.h_5.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionHumidityPmvEN16798.h_1.value,
}

pmv_en_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRatePmvEN16798.h_1.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_2.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_3.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_4.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_5.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRatePmvEN16798.h_1.value,
}

pmv_en_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionClothingPmvEN16798.c_1.value,
        ModelInputsSelectionClothingPmvEN16798.c_2.value,
        ModelInputsSelectionClothingPmvEN16798.c_3.value,
        ModelInputsSelectionClothingPmvEN16798.c_4.value,
        ModelInputsSelectionClothingPmvEN16798.c_5.value,
        ModelInputsSelectionClothingPmvEN16798.c_6.value,
        ModelInputsSelectionClothingPmvEN16798.c_7.value,
        ModelInputsSelectionClothingPmvEN16798.c_8.value,
        ModelInputsSelectionClothingPmvEN16798.c_9.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionClothingPmvEN16798.c_1.value,
}


def Ash55_air_speed_selection():
    return generate_dropdown_inline(adaptive_ashare_air_speed, clearable=False)


def En16798_air_speed_selection():
    return generate_dropdown_inline(adaptive_en_air_speed, clearable=False)

def En16798_relative_humidity_selection():
    return generate_dropdown_inputs_inline(pmv_en_humidity_selection,clearable=False)

def En16798_relative_metabolic_selection():
    return generate_dropdown_inputs_inline(pmv_en_metabolic_selection,clearable=False)

def En16798_relative_clothing_selection():
    return generate_dropdown_inputs_inline(pmv_en_clothing_selection,clearable=False)

