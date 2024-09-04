from scipy._lib.cobyqa.models import Models
from dash import no_update
from components.drop_down_inline import (
    generate_dropdown_inline,
    generate_dropdown_inputs_inline,
)
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
        CHARTS.psychrometric_operative.value,
        CHARTS.relative_humidity.value,
        CHARTS.air_speed.value,
        CHARTS.thermal_heat.value,
        CHARTS.set_outputs.value,
    ],
    "multi": False,
    "default": CHARTS.psychrometric.value,
}

pmv_en_chart = {
    "id": ElementsIDs.CHART_SELECTION.value,
    "question": TextHome.chart_selection.value,
    "options": [
        CHARTS.psychrometric.value,
        CHARTS.psychrometric_operative.value,
        CHARTS.relative_humidity.value,
    ],
    "multi": False,
    "default": CHARTS.psychrometric.value,
}


def chart_selection(selected_model, chart_content):
    chart_inputs = ashare_chart
    current_value = None
    if selected_model == MODELS.PMV_ashrae.value:
        chart_inputs = ashare_chart
        current_value = (
            chart_content if chart_content is not None else CHARTS.psychrometric.value
        )
    elif selected_model == MODELS.Adaptive_ashrae.value:
        return
    elif selected_model == MODELS.Adaptive_EN.value:
        return
    elif selected_model == MODELS.PMV_EN.value:
        chart_inputs = pmv_en_chart
        current_value = (
            chart_content if chart_content is not None else CHARTS.psychrometric.value
        )
    elif selected_model == MODELS.Fans_heat.value:
        return
    elif selected_model == MODELS.Phs.value:
        return

    return generate_dropdown_inline(chart_inputs, value=current_value, clearable=False)


adaptive_ashare_air_speed = {
    "id": ElementsIDs.ADAPTIVE_ASHARE_SPEED_SELECTION.value,
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
    "id": ElementsIDs.PMV_EN_HUMIDITY_SELECTION.value,
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
    "id": ElementsIDs.PMV_ENMETABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRatePmvEN16798.h_1.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_2.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_3.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_4.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_5.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_6.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_7.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_8.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_9.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_10.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_11.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_12.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_13.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_14.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_15.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_16.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_17.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_18.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_19.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_20.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_21.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_22.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_23.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_24.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_25.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_26.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_27.value,
        ModelInputsSelectionMetablicRatePmvEN16798.h_28.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRatePmvEN16798.h_1.value,
}

pmv_en_clothing_selection = {
    "id": ElementsIDs.PMV_EN_CLOTHING_SELECTION.value,
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
    "id": ElementsIDs.FANS_AND_HEAT_METABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRateFansAndHeat.h_1.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_2.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_3.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_4.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_5.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_6.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_7.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_8.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_9.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_10.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_11.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_12.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_13.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_14.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_15.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_16.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_17.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_18.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_19.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_20.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_21.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_22.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_23.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_24.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_25.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_26.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_27.value,
        ModelInputsSelectionMetablicRateFansAndHeat.h_28.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRateFansAndHeat.h_1.value,
}

fans_and_heat_clothing_selection = {
    "id": ElementsIDs.FANS_AND_HEAT_CLOTHING_SELECTION.value,
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
    "id": ElementsIDs.PHS_METABOLIC_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetablicRatePhs.h_1.value,
        ModelInputsSelectionMetablicRatePhs.h_2.value,
        ModelInputsSelectionMetablicRatePhs.h_3.value,
        ModelInputsSelectionMetablicRatePhs.h_4.value,
        ModelInputsSelectionMetablicRatePhs.h_5.value,
        ModelInputsSelectionMetablicRatePhs.h_6.value,
        ModelInputsSelectionMetablicRatePhs.h_7.value,
        ModelInputsSelectionMetablicRatePhs.h_8.value,
        ModelInputsSelectionMetablicRatePhs.h_9.value,
        ModelInputsSelectionMetablicRatePhs.h_10.value,
        ModelInputsSelectionMetablicRatePhs.h_11.value,
        ModelInputsSelectionMetablicRatePhs.h_12.value,
        ModelInputsSelectionMetablicRatePhs.h_13.value,
        ModelInputsSelectionMetablicRatePhs.h_14.value,
        ModelInputsSelectionMetablicRatePhs.h_15.value,
        ModelInputsSelectionMetablicRatePhs.h_16.value,
        ModelInputsSelectionMetablicRatePhs.h_17.value,
        ModelInputsSelectionMetablicRatePhs.h_18.value,
        ModelInputsSelectionMetablicRatePhs.h_19.value,
        ModelInputsSelectionMetablicRatePhs.h_20.value,
        ModelInputsSelectionMetablicRatePhs.h_21.value,
        ModelInputsSelectionMetablicRatePhs.h_22.value,
        ModelInputsSelectionMetablicRatePhs.h_23.value,
        ModelInputsSelectionMetablicRatePhs.h_24.value,
        ModelInputsSelectionMetablicRatePhs.h_25.value,
        ModelInputsSelectionMetablicRatePhs.h_26.value,
        ModelInputsSelectionMetablicRatePhs.h_27.value,
        ModelInputsSelectionMetablicRatePhs.h_28.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetablicRatePhs.h_1.value,
}

phs_clothing_selection = {
    "id": ElementsIDs.PHS_CLOTHING_SELECTION.value,
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

pmv_ashrae_speed_selection = {
    "id": ElementsIDs.PMV_ASHARE_SPEED_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionSpeedASHRAE55.s_1.value,
        ModelInputsSelectionSpeedASHRAE55.s_2.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionSpeedASHRAE55.s_1.value,
}

pmv_ashrae_humidity_selection = {
    "id": ElementsIDs.PMV_ASHARE_Humidity_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionhumidityASHRAE55.h_1.value,
        ModelInputsSelectionhumidityASHRAE55.h_2.value,
        ModelInputsSelectionhumidityASHRAE55.h_3.value,
        ModelInputsSelectionhumidityASHRAE55.h_4.value,
        ModelInputsSelectionhumidityASHRAE55.h_5.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionhumidityASHRAE55.h_1.value,
}

pmv_ashrae_metabolic_selection = {
    "id": ElementsIDs.PMV_ASHARE_Metabolic_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionMetabolicASHRAE55.h_1.value,
        ModelInputsSelectionMetabolicASHRAE55.h_2.value,
        ModelInputsSelectionMetabolicASHRAE55.h_3.value,
        ModelInputsSelectionMetabolicASHRAE55.h_4.value,
        ModelInputsSelectionMetabolicASHRAE55.h_5.value,
        ModelInputsSelectionMetabolicASHRAE55.h_6.value,
        ModelInputsSelectionMetabolicASHRAE55.h_7.value,
        ModelInputsSelectionMetabolicASHRAE55.h_8.value,
        ModelInputsSelectionMetabolicASHRAE55.h_9.value,
        ModelInputsSelectionMetabolicASHRAE55.h_10.value,
        ModelInputsSelectionMetabolicASHRAE55.h_11.value,
        ModelInputsSelectionMetabolicASHRAE55.h_12.value,
        ModelInputsSelectionMetabolicASHRAE55.h_13.value,
        ModelInputsSelectionMetabolicASHRAE55.h_14.value,
        ModelInputsSelectionMetabolicASHRAE55.h_15.value,
        ModelInputsSelectionMetabolicASHRAE55.h_16.value,
        ModelInputsSelectionMetabolicASHRAE55.h_17.value,
        ModelInputsSelectionMetabolicASHRAE55.h_18.value,
        ModelInputsSelectionMetabolicASHRAE55.h_19.value,
        ModelInputsSelectionMetabolicASHRAE55.h_20.value,
        ModelInputsSelectionMetabolicASHRAE55.h_21.value,
        ModelInputsSelectionMetabolicASHRAE55.h_22.value,
        ModelInputsSelectionMetabolicASHRAE55.h_23.value,
        ModelInputsSelectionMetabolicASHRAE55.h_24.value,
        ModelInputsSelectionMetabolicASHRAE55.h_25.value,
        ModelInputsSelectionMetabolicASHRAE55.h_26.value,
        ModelInputsSelectionMetabolicASHRAE55.h_27.value,
        ModelInputsSelectionMetabolicASHRAE55.h_28.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionMetabolicASHRAE55.h_1.value,
}

pmv_ashare_clothing_selection = {
    "id": ElementsIDs.PMV_ASHARE_Clothing_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionClothingASHRAE55.c_1.value,
        ModelInputsSelectionClothingASHRAE55.c_2.value,
        ModelInputsSelectionClothingASHRAE55.c_3.value,
        ModelInputsSelectionClothingASHRAE55.c_4.value,
        ModelInputsSelectionClothingASHRAE55.c_5.value,
        ModelInputsSelectionClothingASHRAE55.c_6.value,
        ModelInputsSelectionClothingASHRAE55.c_7.value,
        ModelInputsSelectionClothingASHRAE55.c_8.value,
        ModelInputsSelectionClothingASHRAE55.c_9.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionClothingASHRAE55.c_1.value,
}


def Ash55_air_speed_selection():
    return generate_dropdown_inputs_inline(adaptive_ashare_air_speed, clearable=False)


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
