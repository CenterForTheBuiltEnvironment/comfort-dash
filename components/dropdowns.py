from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, MODELS, CHARTS
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
