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
        AdaptiveENSpeeds.lower_than_06.value,
        AdaptiveENSpeeds.speed_06.value,
        AdaptiveENSpeeds.speed_09.value,
        AdaptiveENSpeeds.speed_12.value,
    ],
    "multi": False,
    "default": AdaptiveENSpeeds.speed_06.value,
}

pmv_en_humidity_selection = {
    "id": ElementsIDs.HUMIDITY_SELECTION.value,
    "question": "",
    "options": [
        HumiditySelection.relative_humidity.value,
        HumiditySelection.humidity_ratio.value,
        HumiditySelection.dew_point.value,
        HumiditySelection.wet_bulb.value,
        HumiditySelection.vapor_pressure.value,
    ],
    "multi": False,
    "default": HumiditySelection.relative_humidity.value,
}

pmv_en_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.seated_quiet.value,
        MetabolicRateSelection.reading_seated.value,
        MetabolicRateSelection.writing.value,
        MetabolicRateSelection.typing.value,
        MetabolicRateSelection.standing_relaxed.value,
        MetabolicRateSelection.filing_seated.value,
        MetabolicRateSelection.flying_aircraft_routine.value,
        MetabolicRateSelection.filing_standing.value,
        MetabolicRateSelection.driving_car.value,
        MetabolicRateSelection.walking_about.value,
        MetabolicRateSelection.cooking.value,
        MetabolicRateSelection.table_sawing.value,
        MetabolicRateSelection.walking_2mph.value,
        MetabolicRateSelection.lifting_packing.value,
        MetabolicRateSelection.seated_heavy_limb_movement.value,
        MetabolicRateSelection.light_machine_work.value,
        MetabolicRateSelection.flying_aircraft_combat.value,
        MetabolicRateSelection.walking_3mph.value,
        MetabolicRateSelection.house_cleaning.value,
        MetabolicRateSelection.driving_heavy_vehicle.value,
        MetabolicRateSelection.dancing.value,
        MetabolicRateSelection.calisthenics.value,
        MetabolicRateSelection.walking_4mph.value,
        MetabolicRateSelection.tennis.value,
        MetabolicRateSelection.heavy_machine_work.value,
        MetabolicRateSelection.handling_100lb_bags.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

pmv_en_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.walking_shorts_short_sleeve.value,
        ClothingSelection.typical_summer_indoor.value,
        ClothingSelection.knee_skirt_short_sleeve.value,
        ClothingSelection.trousers_short_sleeve.value,
        ClothingSelection.trousers_long_sleeve.value,
        ClothingSelection.knee_skirt_long_sleeve.value,
        ClothingSelection.sweat_pants_sweatshirt.value,
        ClothingSelection.jacket_trousers_long_sleeve.value,
        ClothingSelection.typical_winter_indoor.value,
    ],
    "multi": False,
    "default": ClothingSelection.walking_shorts_short_sleeve.value,
}

fans_and_heat_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.seated_quiet.value,
        MetabolicRateSelection.reading_seated.value,
        MetabolicRateSelection.writing.value,
        MetabolicRateSelection.typing.value,
        MetabolicRateSelection.standing_relaxed.value,
        MetabolicRateSelection.filing_seated.value,
        MetabolicRateSelection.flying_aircraft_routine.value,
        MetabolicRateSelection.filing_standing.value,
        MetabolicRateSelection.driving_car.value,
        MetabolicRateSelection.walking_about.value,
        MetabolicRateSelection.cooking.value,
        MetabolicRateSelection.table_sawing.value,
        MetabolicRateSelection.walking_2mph.value,
        MetabolicRateSelection.lifting_packing.value,
        MetabolicRateSelection.seated_heavy_limb_movement.value,
        MetabolicRateSelection.light_machine_work.value,
        MetabolicRateSelection.flying_aircraft_combat.value,
        MetabolicRateSelection.walking_3mph.value,
        MetabolicRateSelection.house_cleaning.value,
        MetabolicRateSelection.driving_heavy_vehicle.value,
        MetabolicRateSelection.dancing.value,
        MetabolicRateSelection.calisthenics.value,
        MetabolicRateSelection.walking_4mph.value,
        MetabolicRateSelection.tennis.value,
        MetabolicRateSelection.heavy_machine_work.value,
        MetabolicRateSelection.handling_100lb_bags.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

fans_and_heat_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.walking_shorts_short_sleeve.value,
        ClothingSelection.typical_summer_indoor.value,
        ClothingSelection.knee_skirt_short_sleeve.value,
        ClothingSelection.trousers_short_sleeve.value,
        ClothingSelection.trousers_long_sleeve.value,
        ClothingSelection.knee_skirt_long_sleeve.value,
        ClothingSelection.sweat_pants_sweatshirt.value,
        ClothingSelection.jacket_trousers_long_sleeve.value,
        ClothingSelection.typical_winter_indoor.value,
    ],
    "multi": False,
    "default": ClothingSelection.walking_shorts_short_sleeve.value,
}

phs_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.seated_quiet.value,
        MetabolicRateSelection.reading_seated.value,
        MetabolicRateSelection.writing.value,
        MetabolicRateSelection.typing.value,
        MetabolicRateSelection.standing_relaxed.value,
        MetabolicRateSelection.filing_seated.value,
        MetabolicRateSelection.flying_aircraft_routine.value,
        MetabolicRateSelection.filing_standing.value,
        MetabolicRateSelection.driving_car.value,
        MetabolicRateSelection.walking_about.value,
        MetabolicRateSelection.cooking.value,
        MetabolicRateSelection.table_sawing.value,
        MetabolicRateSelection.walking_2mph.value,
        MetabolicRateSelection.lifting_packing.value,
        MetabolicRateSelection.seated_heavy_limb_movement.value,
        MetabolicRateSelection.light_machine_work.value,
        MetabolicRateSelection.flying_aircraft_combat.value,
        MetabolicRateSelection.walking_3mph.value,
        MetabolicRateSelection.house_cleaning.value,
        MetabolicRateSelection.driving_heavy_vehicle.value,
        MetabolicRateSelection.dancing.value,
        MetabolicRateSelection.calisthenics.value,
        MetabolicRateSelection.walking_4mph.value,
        MetabolicRateSelection.tennis.value,
        MetabolicRateSelection.heavy_machine_work.value,
        MetabolicRateSelection.handling_100lb_bags.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

phs_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.walking_shorts_short_sleeve.value,
        ClothingSelection.typical_summer_indoor.value,
        ClothingSelection.knee_skirt_short_sleeve.value,
        ClothingSelection.trousers_short_sleeve.value,
        ClothingSelection.trousers_long_sleeve.value,
        ClothingSelection.knee_skirt_long_sleeve.value,
        ClothingSelection.sweat_pants_sweatshirt.value,
        ClothingSelection.jacket_trousers_long_sleeve.value,
        ClothingSelection.typical_winter_indoor.value,
    ],
    "multi": False,
    "default": ClothingSelection.walking_shorts_short_sleeve.value,
}

pmv_ashrae_speed_selection = {
    "id": ElementsIDs.PMV_ASHRAE_SPEED_SELECTION.value,
    "question": "",
    "options": [
        ModelInputsSelectionSpeedASHRAE55.no_local_control.value,
        ModelInputsSelectionSpeedASHRAE55.local_control.value,
    ],
    "multi": False,
    "default": ModelInputsSelectionSpeedASHRAE55.no_local_control.value,
}

pmv_ashrae_humidity_selection = {
    "id": ElementsIDs.HUMIDITY_SELECTION.value,
    "question": "",
    "options": [
        HumiditySelection.relative_humidity.value,
        HumiditySelection.humidity_ratio.value,
        HumiditySelection.dew_point.value,
        HumiditySelection.wet_bulb.value,
        HumiditySelection.vapor_pressure.value,
    ],
    "multi": False,
    "default": HumiditySelection.relative_humidity.value,
}

pmv_ashrae_metabolic_selection = {
    "id": ElementsIDs.METABOLIC_RATE_SELECTION.value,
    "question": "",
    "options": [
        MetabolicRateSelection.sleeping.value,
        MetabolicRateSelection.reclining.value,
        MetabolicRateSelection.seated_quiet.value,
        MetabolicRateSelection.reading_seated.value,
        MetabolicRateSelection.writing.value,
        MetabolicRateSelection.typing.value,
        MetabolicRateSelection.standing_relaxed.value,
        MetabolicRateSelection.filing_seated.value,
        MetabolicRateSelection.flying_aircraft_routine.value,
        MetabolicRateSelection.filing_standing.value,
        MetabolicRateSelection.driving_car.value,
        MetabolicRateSelection.walking_about.value,
        MetabolicRateSelection.cooking.value,
        MetabolicRateSelection.table_sawing.value,
        MetabolicRateSelection.walking_2mph.value,
        MetabolicRateSelection.lifting_packing.value,
        MetabolicRateSelection.seated_heavy_limb_movement.value,
        MetabolicRateSelection.light_machine_work.value,
        MetabolicRateSelection.flying_aircraft_combat.value,
        MetabolicRateSelection.walking_3mph.value,
        MetabolicRateSelection.house_cleaning.value,
        MetabolicRateSelection.driving_heavy_vehicle.value,
        MetabolicRateSelection.dancing.value,
        MetabolicRateSelection.calisthenics.value,
        MetabolicRateSelection.walking_4mph.value,
        MetabolicRateSelection.tennis.value,
        MetabolicRateSelection.heavy_machine_work.value,
        MetabolicRateSelection.handling_100lb_bags.value,
    ],
    "multi": False,
    "default": MetabolicRateSelection.sleeping.value,
}

pmv_ashare_clothing_selection = {
    "id": ElementsIDs.CLOTHING_SELECTION.value,
    "question": "",
    "options": [
        ClothingSelection.walking_shorts_short_sleeve.value,
        ClothingSelection.typical_summer_indoor.value,
        ClothingSelection.knee_skirt_short_sleeve.value,
        ClothingSelection.trousers_short_sleeve.value,
        ClothingSelection.trousers_long_sleeve.value,
        ClothingSelection.knee_skirt_long_sleeve.value,
        ClothingSelection.sweat_pants_sweatshirt.value,
        ClothingSelection.jacket_trousers_long_sleeve.value,
        ClothingSelection.typical_winter_indoor.value,
    ],
    "multi": False,
    "default": ClothingSelection.walking_shorts_short_sleeve.value,
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
