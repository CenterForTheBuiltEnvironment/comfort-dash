from scipy._lib.cobyqa.models import Models

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import (
    ElementsIDs,
    MODELS,
    CHARTS,
    AdaptiveAshraeSpeeds,
    AdaptiveENSpeeds,
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

    if selected_model == "PMV - ASHRAE 55":
        chart_inputs = ashare_chart
    elif selected_model == "Adaptive - ASHRAE 55":
        return
    elif selected_model == "Adaptive - EN 16798":
        return
    elif selected_model == "PMV - EN 16798":
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


def Ash55_air_speed_selection():
    return generate_dropdown_inline(adaptive_ashare_air_speed, clearable=False)


def En16798_air_speed_selection():
    return generate_dropdown_inline(adaptive_en_air_speed, clearable=False)
