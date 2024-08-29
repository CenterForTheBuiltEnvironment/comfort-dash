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
    ModelInputsSelectionClothingPmvEN16798,
    ModelInputsSelectionMetablicRateFansAndHeat,
    ModelInputsSelectionClothingFansAndHeat,
    ModelInputsSelectionMetablicRatePhs,
    ModelInputsSelectionClothingPhs,
    ModelInputsSelectionSpeedASHRAE55,
    ModelInputsSelectionhumidityASHRAE55,
    ModelInputsSelectionMetabolicASHRAE55,
    ModelInputsSelectionClothingASHRAE55,
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
        MODELS.Fans_heat.value,
        MODELS.Phs.value,
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
        return
    elif selected_model == MODELS.Fans_heat.value:
        return
    elif selected_model == MODELS.Phs.value:
        return

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

fans_and_heat_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRateFansAndHeat.h_1.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_2.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_3.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_4.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_5.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRateFansAndHeat.h_1.value,
}

fans_and_heat_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionClothingFansAndHeat.c_1.value,
        ModelInputsSelectionClothingFansAndHeat.c_2.value,
        ModelInputsSelectionClothingFansAndHeat.c_3.value,
        ModelInputsSelectionClothingFansAndHeat.c_4.value,
        ModelInputsSelectionClothingFansAndHeat.c_5.value,
        ModelInputsSelectionClothingFansAndHeat.c_6.value,
        ModelInputsSelectionClothingFansAndHeat.c_7.value,
        ModelInputsSelectionClothingFansAndHeat.c_8.value,
        ModelInputsSelectionClothingFansAndHeat.c_9.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionClothingFansAndHeat.c_1.value,
}

phs_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRatePhs.h_1.value,
        ModelInputsSelectionMetablicRatePhs.h_2.value,
        ModelInputsSelectionMetablicRatePhs.h_3.value,
        ModelInputsSelectionMetablicRatePhs.h_4.value,
        ModelInputsSelectionMetablicRatePhs.h_5.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRatePhs.h_1.value,
}

phs_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionClothingPhs.c_1.value,
        ModelInputsSelectionClothingPhs.c_2.value,
        ModelInputsSelectionClothingPhs.c_3.value,
        ModelInputsSelectionClothingPhs.c_4.value,
        ModelInputsSelectionClothingPhs.c_5.value,
        ModelInputsSelectionClothingPhs.c_6.value,
        ModelInputsSelectionClothingPhs.c_7.value,
        ModelInputsSelectionClothingPhs.c_8.value,
        ModelInputsSelectionClothingPhs.c_9.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionClothingPhs.c_1.value,
}

ModelInputsSelectionSpeedASHRAE55List ={
    "id": ElementsIDs.SPEED_Method.value,
    "question": "",
    "options": [
        ModelInputsSelectionSpeedASHRAE55.s_1.value,
        ModelInputsSelectionSpeedASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionSpeedASHRAE55.s_1.value,
}

ModelInputsSelectionhumidityASHRAE55List ={
    "id": ElementsIDs.Humidity_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionhumidityASHRAE55.s_1.value,
        ModelInputsSelectionhumidityASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionhumidityASHRAE55.s_1.value,
}

ModelInputsSelectionMetabolicASHRAE55List ={
    "id": ElementsIDs.Metabolic_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetabolicASHRAE55.s_1.value,
        ModelInputsSelectionMetabolicASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetabolicASHRAE55.s_1.value,
}

ModelInputsSelectionClothingASHRAE55List ={
    "id": ElementsIDs.Clothing_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionClothingASHRAE55.s_1.value,
        ModelInputsSelectionClothingASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionClothingASHRAE55.s_1.value,
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

def Fans_heat_metabolic_selection():
    return generate_dropdown_inputs_inline(fans_and_heat_metabolic_selection, clearable=False)

def Fans_heat_clothing_selection():
    return generate_dropdown_inputs_inline(fans_and_heat_clothing_selection, clearable=False)

def Phs_metabolic_selection():
    return generate_dropdown_inputs_inline(fans_and_heat_metabolic_selection, clearable=False)

def Phs_clothing_selection():
    return generate_dropdown_inputs_inline(fans_and_heat_clothing_selection, clearable=False)

def ModelInputsSelectionSpeedASHRAE55List_selection():
    return generate_dropdown_inputs_inline(ModelInputsSelectionSpeedASHRAE55List, clearable=False)

def ModelInputsSelectionhumidityASHRAE55List_selection():
    return generate_dropdown_inputs_inline(ModelInputsSelectionhumidityASHRAE55List, clearable=False)

def ModelInputsSelectionMetabolicASHRAE55List_selection():
    return generate_dropdown_inputs_inline(ModelInputsSelectionMetabolicASHRAE55List, clearable=False)

def ModelInputsSelectionClothingASHRAE55List_selection():
    return generate_dropdown_inputs_inline(ModelInputsSelectionClothingASHRAE55List, clearable=False)