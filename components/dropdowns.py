from scipy._lib.cobyqa.models import Models

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, MODELS, CHARTS, SPEEDS
from utils.website_text import TextHome

dd_model = {
    "id": ElementsIDs.MODEL_SELECTION.value,
    "question": TextHome.model_selection.value,
    "options": [MODELS.PMV.value, MODELS.Adaptive.value, MODELS.EN.value],
    "multi": False,
    "default": MODELS.PMV.value,
}


def model_selection():
    return generate_dropdown_inline(dd_model, clearable=False)


dd_chart = {
    "id": ElementsIDs.CHART_SELECTION.value,
    "question": TextHome.chart_selection.value,
    "options": [CHARTS.t_rh.value, CHARTS.psychrometric.value],
    "multi": False,
    "default": CHARTS.t_rh.value,
}


def chart_selection():
    return generate_dropdown_inline(dd_chart, clearable=False)


dd_speed = {
    "id": ElementsIDs.SPEED_SELECTION.value,
    "question": TextHome.speed_selection.value,
    "options": [SPEEDS.s_1.value, SPEEDS.s_2.value, SPEEDS.S_3.value, SPEEDS.s_4.value],
    "multi": False,
    "default": SPEEDS.s_1.value,

}
def Ash55_air_speed_selection():
    return generate_dropdown_inline(dd_speed, clearable=False)
