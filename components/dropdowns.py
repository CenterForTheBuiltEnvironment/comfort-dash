from components.drop_down_inline import (
    generate_dropdown_inline,
)
from utils.my_config_file import (
    ElementsIDs,
    Models,
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
