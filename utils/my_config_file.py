import platform
from enum import Enum
from pydantic import BaseModel


class Dimensions(Enum):
    default_container_width = "md"
    left_container_width = 5
    right_container_width = 7


class ElementsIDs(Enum):
    NAVBAR = "id-navbar"
    NAVBAR_COLLAPSE = "navbar-collapse"
    NAVBAR_TOGGLER = "navbar-toggle"
    NAVBAR_BURGER_BUTTON = "burger-button"
    NAVBAR_ID_HOME = "id-nav-home"
    NAVBAR_ID_SETTINGS = "id-nav-settings"
    NAVBAR_ID_ABOUT = "id-nav-about"
    MODEL_SELECTION = "id-model-selection"
    CHART_SELECTION = "id-chart-selection"
    CHART_CONTAINER = "id-chart-container"
    URL = "url"
    FOOTER = "id-footer"
    NAVBAR_ID_DOCUMENT = "id-nav-documentation"
    NAVBAR_ID_MORE_CBE_TOOLS = "id-nav-more-cbe-tools"
    ADAPTIVE_ASHARE_SPEED_SELECTION = "id-adaptive-ashare-speed-selection"
    ADAPTIVE_EN_SPEED_SELECTION = "id-adaptive-en-speed-selection"
    PMV_EN_HUMIDITY_SELECTION = "id-humidity-selection"
    PMV_EN_METABOLIC_SELECTION = "id-metabolic-selection"
    PMV_EN_CLOTHING_SELECTION = "id-clothing-selection"
    FANS_AND_HEAT_METABOLIC_SELECTION = "id-fans-and-heat-metabolic-selection"
    FANS_AND_HEAT_CLOTHING_SELECTION = "id-fans-and-heat-clothing-selection"
    PHS_METABOLIC_SELECTION = "id-phs-metabolic-selection"
    PHS_CLOTHING_SELECTION = "id-phs-clothing-selection"
    PMV_ASHRAE_SPEED_SELECTION = "id-pmv-ashrae-speed-method"
    PMV_ASHARE_Humidity_SELECTION = "id-pmv-ashrae-humidity-method"
    PMV_ASHARE_Metabolic_SELECTION = "id-pmv-ashrae-metabolic-method"
    PMV_ASHARE_Clothing_SELECTION = "id-pmv-ashrae-clothing-method"


class Config(Enum):
    # DEBUG: bool = False
    DEBUG: bool = "macOS" in platform.platform() or "Windows" in platform.platform()


class Functionalities(Enum):
    Default: str = "Default"
    Compare: str = "Compare"
    Ranges: str = "Ranges"


class URLS(Enum):
    HOME: str = "/"
    ABOUT: str = "/about"
    DOCUMENTAION: str = "/documentation"
    TOOLS: str = "/moreCBETools"


class ToolUrls(Enum):
    cbe_thermal_comfort_tool: str = (
        "https://cbe.berkeley.edu/research/cbe-thermal-comfort-tool/"
    )
    clima_tool: str = "https://cbe.berkeley.edu/research/clima-tool/"
    advance_ceiling_fan_design_tool: str = (
        "https://cbe.berkeley.edu/research/advanced-ceiling-fan-design-tool/"
    )
    guidebook_on_fans_for_cooling_people_tool: str = (
        "https://cbe.berkeley.edu/research/guidebook-on-fans-for-cooling-people/"
    )
    occupant_survey_and_building_benchmarking_tool: str = (
        "https://cbe.berkeley.edu/research/occupant-survey-and-building-benchmarking/"
    )
    cbe_rad_tool_early_design_tool_for_high_thermal_mass_radiant_syste_tool: str = (
        "https://cbe.berkeley.edu/research/cbe-rad-tool-early-design-tool-for-high-thermal-mass-radiant-systems/"
    )
    setpoint_energy_savings_calculator_tool: str = (
        "https://cbe.berkeley.edu/research/setpoint-energy-savings-calculator/"
    )
    cbe_3d_mean_radiant_temperature_tool: str = (
        "https://cbe.berkeley.edu/research/cbe-3d-mean-radiant-temperature-tool/"
    )
    underfloor_air_distribution_ufad_cooling_load_design_tool: str = (
        "https://cbe.berkeley.edu/research/underfloor-air-distribution-ufad-cooling-load-design-tool/"
    )
    global_comfort_data_visualization_tool: str = (
        "https://cbe.berkeley.edu/research/global-comfort-data-visualization-tools/"
    )
    python_package_for_thermal_comfort_tool: str = (
        "https://cbe.berkeley.edu/research/python-package-for-thermal-comfort/"
    )
    energy_performance_modeling_underfloor_air_distribution_systems_tool: str = (
        "https://cbe.berkeley.edu/research/energy-performance-modeling-underfloor-air-distribution-systems/"
    )


class Stores(Enum):
    INPUT_DATA = "store_input_data"


class MODELS(Enum):
    PMV_ashrae: str = "PMV - ASHRAE 55"
    PMV_EN: str = "PMV - EN 16798"
    Adaptive_ashrae: str = "Adaptive - ASHRAE 55"
    Adaptive_EN: str = "Adaptive - EN 16798"
    Fans_heat: str = "FANS & HEAT"
    Phs: str = "PHS"


class CHARTS(Enum):
    t_rh: str = "Temperature and Relative Humidity"
    psychrometric: str = "Psychrometric (air temperature)"
    psychrometric_operative: str = "Psychrometric (operative temperature)"
    relative_humidity: str = "Relative humidity vs. air temperature"
    air_speed: str = "Air speed vs. operative temperature"
    thermal_heat: str = "Thermal heat losses vs. air temperature"
    set_outputs: str = "SET outputs chart"
    fans_Heat_Chart: str = "Fans and Heat Chart"
    phs_Chart: str = "PHS Chart"


class AdaptiveEN(Enum):
    class_I: str = (
        "Class I acceptability limits = Operative temperature: 24.1 to 29.1 °C"
    )
    class_II: str = (
        "Class II acceptability limits = Operative temperature: 23.1 to 30.1 °C"
    )
    class_III: str = (
        "Class III acceptability limits = Operative temperature: 22.1 to 31.1 °C"
    )
    adaptive_chart: str = "Adaptive chart"


class AdaptiveAshrae(Enum):
    acceptability_limits_80: str = (
        "80% acceptability limits = Operative temperature: 22.1 to 29.1 °C"
    )
    acceptability_limits_90: str = (
        "90% acceptability limits = Operative temperature: 23.1 to 28.1 °C"
    )
    adaptive_chart: str = "Adaptive chart"


class PmvAshraeResultCard(Enum):
    pmv: str = "PMV = -0.16"
    ppd: str = "PPD = 6 %"
    sensation: str = "Sensation = Neutral"
    set: str = "SET = 24.8 °C"


class PmvENResultCard(Enum):
    pmv: str = "PMV = -0.16"
    ppd: str = "PPD = 6 %"
    set: str = "SET = |"


class PhsResultCard(Enum):
    line1: str = (
        "Maximum allowable exposure time within which the physiological strain is acceptable (no physical damage is to be expected) calculated as a function of:"
    )
    line2: str = "max rectal temperature = 53 min"
    line3: str = "water loss of 5% of the body mass for 95% of the population = 256 min"
    line4: str = "water loss of 7.5% of the body mass for an average person = 380 min"


class ModelInputsInfo(BaseModel):
    name: str
    unit: str
    min: float
    max: float
    step: float
    value: float


class AdaptiveAshraeSpeeds(Enum):
    s_1: str = "0.3 m/s (59fpm)"
    s_2: str = "0.6 m/s (118fpm)"
    S_3: str = "0.9 m/s (177fpm)"
    s_4: str = "1.2 m/s (236fpm)"


class AdaptiveENSpeeds(Enum):
    # todo use the right punctuation and upper case
    # todo the keys should be informative
    s_1: str = "lower than 0.6 m/s (118fpm)"
    s_2: str = "0.6 m/s (118fpm)"
    S_3: str = "0.9 m/s (177fpm)"
    s_4: str = "1.2 m/s (236fpm)"


class ModelInputsPmvAshrae55(BaseModel):
    TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=0.0, max=50.0, step=0.5, value=25.0, name="Air Temperature"
    )
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=4.0, step=0.1, value=0.1, name="Air Speed"
    )
    RH: ModelInputsInfo = ModelInputsInfo(
        unit="%", min=0.0, max=100.0, step=1.0, value=50.0, name="Relative Humidity"
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=0.7, max=4.0, step=0.1, value=1.0, name="Metabolic Rate"
    )
    CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo", min=0.0, max=4.0, step=0.1, value=0.61, name="Clothing Level"
    )


class ModelInputsAdaptiveAshrae55(BaseModel):
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=0.0, max=50.0, step=0.5, value=25.0, name="Air Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=10.0,
        max=35.0,
        step=0.5,
        value=25.0,
        name="Prevailing mean outdoor temperature",
    )


class ModelInputsPmvEN16798(BaseModel):
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=0.0, max=50.0, step=0.5, value=25.0, name="Air Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=0.0,
        max=50.0,
        step=0.5,
        value=25.0,
        name="Mean Radiant Temperature",
    )
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=4.0, step=0.1, value=0.1, name="Air Speed"
    )
    RH: ModelInputsInfo = ModelInputsInfo(
        unit="%", min=0.0, max=100.0, step=1.0, value=50.0, name="Relative Humidity"
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=0.7, max=4.0, step=0.1, value=1, name="Metabolic Rate"
    )
    DYNAMIC_CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo",
        min=0.0,
        max=4.0,
        step=0.1,
        value=0.61,
        name="Dynamic Clothing insulation",
    )


class ModelInputsAdaptiveEN16798(BaseModel):
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=0.0, max=50.0, step=0.5, value=25.0, name="Air Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=0.0,
        max=50.0,
        step=0.5,
        value=25.0,
        name="Mean Radiant Temperature",
    )
    RUNNING_MEAN_OUTDOOR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=10.0,
        max=35.0,
        step=0.1,
        value=25.0,
        name="Running Mean Outdoor Temperature",
    )


class ModelInputsFansHeat(BaseModel):
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=4.5, step=0.1, value=0.8, name="Air Speed"
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=0.7, max=1.9, step=0.1, value=1.1, name="Metabolic Rate"
    )
    CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo", min=0.0, max=0.6, step=0.1, value=0.5, name="Clothing Level"
    )


class ModelInputsPhs(BaseModel):
    # todo the model inputs should be taken from a global class, we then should update the min and max values
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=15.0, max=50.0, step=0.5, value=25.0, name="Air Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=15.0,
        max=50.0,
        step=0.5,
        value=25.0,
        name="Mean Radiant Temperature",
    )
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=3.0, step=0.1, value=0.1, name="Air Speed"
    )
    RH: ModelInputsInfo = ModelInputsInfo(
        unit="%", min=0.0, max=100.0, step=1.0, value=50.0, name="Relative Humidity"
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=1.0, max=4.3, step=0.1, value=1.2, name="Metabolic Rate"
    )
    CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo", min=0.1, max=1.0, step=0.1, value=0.5, name="Clothing Level"
    )


# PMV - Ashare right selection
class ModelInputsSelectionSpeedASHRAE55(Enum):
    s_1: str = "No local control"
    s_2: str = "with local control"


class ModelInputsSelectionHumidityASHRAE55(Enum):
    # todo pycharm is telling me that this code is duplicated
    h_1: str = "Relative humidity"
    h_2: str = "Humidity ratio"
    h_3: str = "Dew point"
    h_4: str = "Wet bulb"
    h_5: str = "Vapor pressure"


class ModelInputsSelectionMetabolicASHRAE55(Enum):
    h_1: str = "Sleeping: 0.7"
    h_2: str = "Reclining"
    h_3: str = "Seated, quite: 1.0"
    h_4: str = "Reading, seated: 1.0"
    h_5: str = "Writing: 1.0"
    h_6: str = "Typing: 1.1"
    h_7: str = "Standing, relaxed: 1.2"
    h_8: str = "Filing, seated: 1.2"
    h_9: str = "Flying aircraft, routine: 1.2"
    h_10: str = "Filing, standing: 1.4"
    h_11: str = "Driving a car: 1.5"
    h_12: str = "Walking about: 1.7"
    h_13: str = "Cooking: 1.8"
    h_14: str = "Table sawing: 1.8"
    h_15: str = "Walking 2mph (3.2kmh): 2.0"
    h_16: str = "Lifting/packing: 2.1"
    h_17: str = "Seated, heavy limb movement: 2.2"
    h_18: str = "Light machine work: 2.2"
    h_19: str = "Flying aircraft, combat: 2.4"
    h_20: str = "Walking 3mph (4.8kmh): 2.6"
    h_21: str = "House cleaning: 2.7"
    h_22: str = "Driving, heavy vehicle: 3.2"
    h_23: str = "Dancing: 3.4"
    h_24: str = "Calisthenics: 3.5"
    h_25: str = "Walking 4mph (6.4kmh): 3.8"
    h_26: str = "Tennis: 3.8"
    h_27: str = "Heavy machine work: 4.0"
    h_28: str = "Handling 100lb (45 kg) bags: 4.0"


class ModelInputsSelectionClothingASHRAE55(Enum):
    c_1: str = "Walking shorts, short-sleeve shirt: 0.36 clo"
    c_2: str = "Typical summer indoor clothing: 0.5 clo"
    c_3: str = "Knee-length skirt, short-sleeve shirt, sandals, underwear: 0.54 clo"
    c_4: str = "Trousers, short-sleeve shirt, socks, shoes, underwear: 0.57 clo"
    c_5: str = "Trousers, long-sleeve shirt: 0.61 clo"
    c_6: str = "Knee-length skirt, long-sleeve shirt, full slip: 0.67 clo"
    c_7: str = "Sweat pants, long-sleeve sweatshirt: 0.74 clo"
    c_8: str = "Jacket, Trousers, long-sleeve shirt: 0.96 clo"
    c_9: str = "Typical winter indoor clothing: 1.0 clo"


# PMV - EN right selectioon
class ModelInputsSelectionHumidityPmvEN16798(Enum):
    h_1: str = "Relative humidity"
    h_2: str = "Humidity ratio"
    h_3: str = "Dew point"
    h_4: str = "Wet bulb"
    h_5: str = "Vapor pressure"


class ModelInputsSelectionMetablicRatePmvEN16798(Enum):
    h_1: str = "Sleeping: 0.7"
    h_2: str = "Reclining"
    h_3: str = "Seated, quite: 1.0"
    h_4: str = "Reading, seated: 1.0"
    h_5: str = "Writing: 1.0"
    h_6: str = "Typing: 1.1"
    h_7: str = "Standing, relaxed: 1.2"
    h_8: str = "Filing, seated: 1.2"
    h_9: str = "Flying aircraft, routine: 1.2"
    h_10: str = "Filing, standing: 1.4"
    h_11: str = "Driving a car: 1.5"
    h_12: str = "Walking about: 1.7"
    h_13: str = "Cooking: 1.8"
    h_14: str = "Table sawing: 1.8"
    h_15: str = "Walking 2mph (3.2kmh): 2.0"
    h_16: str = "Lifting/packing: 2.1"
    h_17: str = "Seated, heavy limb movement: 2.2"
    h_18: str = "Light machine work: 2.2"
    h_19: str = "Flying aircraft, combat: 2.4"
    h_20: str = "Walking 3mph (4.8kmh): 2.6"
    h_21: str = "House cleaning: 2.7"
    h_22: str = "Driving, heavy vehicle: 3.2"
    h_23: str = "Dancing: 3.4"
    h_24: str = "Calisthenics: 3.5"
    h_25: str = "Walking 4mph (6.4kmh): 3.8"
    h_26: str = "Tennis: 3.8"
    h_27: str = "Heavy machine work: 4.0"
    h_28: str = "Handling 100lb (45 kg) bags: 4.0"


class ModelInputsSelectionClothingPmvEN16798(Enum):
    c_1: str = "Walking shorts, short-sleeve shirt: 0.36 clo"
    c_2: str = "Typical summer indoor clothing: 0.5 clo"
    c_3: str = "Knee-length skirt, short-sleeve shirt, sandals, underwear: 0.54 clo"
    c_4: str = "Trousers, short-sleeve shirt, socks, shoes, underwear: 0.57 clo"
    c_5: str = "Trousers, long-sleeve shirt: 0.61 clo"
    c_6: str = "Knee-length skirt, long-sleeve shirt, full slip: 0.67 clo"
    c_7: str = "Sweat pants, long-sleeve sweatshirt: 0.74 clo"
    c_8: str = "Jacket, Trousers, long-sleeve shirt: 0.96 clo"
    c_9: str = "Typical winter indoor clothing: 1.0 clo"


# Fans and Heat right selection
class ModelInputsSelectionMetablicRateFansAndHeat(Enum):
    h_1: str = "Sleeping: 0.7"
    h_2: str = "Reclining"
    h_3: str = "Seated, quite: 1.0"
    h_4: str = "Reading, seated: 1.0"
    h_5: str = "Writing: 1.0"
    h_6: str = "Typing: 1.1"
    h_7: str = "Standing, relaxed: 1.2"
    h_8: str = "Filing, seated: 1.2"
    h_9: str = "Flying aircraft, routine: 1.2"
    h_10: str = "Filing, standing: 1.4"
    h_11: str = "Driving a car: 1.5"
    h_12: str = "Walking about: 1.7"
    h_13: str = "Cooking: 1.8"
    h_14: str = "Table sawing: 1.8"
    h_15: str = "Walking 2mph (3.2kmh): 2.0"
    h_16: str = "Lifting/packing: 2.1"
    h_17: str = "Seated, heavy limb movement: 2.2"
    h_18: str = "Light machine work: 2.2"
    h_19: str = "Flying aircraft, combat: 2.4"
    h_20: str = "Walking 3mph (4.8kmh): 2.6"
    h_21: str = "House cleaning: 2.7"
    h_22: str = "Driving, heavy vehicle: 3.2"
    h_23: str = "Dancing: 3.4"
    h_24: str = "Calisthenics: 3.5"
    h_25: str = "Walking 4mph (6.4kmh): 3.8"
    h_26: str = "Tennis: 3.8"
    h_27: str = "Heavy machine work: 4.0"
    h_28: str = "Handling 100lb (45 kg) bags: 4.0"


class ModelInputsSelectionClothingFansAndHeat(Enum):
    c_1: str = "Walking shorts, short-sleeve shirt: 0.36 clo"
    c_2: str = "Typical summer indoor clothing: 0.5 clo"
    c_3: str = "Knee-length skirt, short-sleeve shirt, sandals, underwear: 0.54 clo"
    c_4: str = "Trousers, short-sleeve shirt, socks, shoes, underwear: 0.57 clo"
    c_5: str = "Trousers, long-sleeve shirt: 0.61 clo"
    c_6: str = "Knee-length skirt, long-sleeve shirt, full slip: 0.67 clo"
    c_7: str = "Sweat pants, long-sleeve sweatshirt: 0.74 clo"
    c_8: str = "Jacket, Trousers, long-sleeve shirt: 0.96 clo"
    c_9: str = "Typical winter indoor clothing: 1.0 clo"


# PHS right selection
class ModelInputsSelectionMetablicRatePhs(Enum):
    h_1: str = "Sleeping: 0.7"
    h_2: str = "Reclining"
    h_3: str = "Seated, quite: 1.0"
    h_4: str = "Reading, seated: 1.0"
    h_5: str = "Writing: 1.0"
    h_6: str = "Typing: 1.1"
    h_7: str = "Standing, relaxed: 1.2"
    h_8: str = "Filing, seated: 1.2"
    h_9: str = "Flying aircraft, routine: 1.2"
    h_10: str = "Filing, standing: 1.4"
    h_11: str = "Driving a car: 1.5"
    h_12: str = "Walking about: 1.7"
    h_13: str = "Cooking: 1.8"
    h_14: str = "Table sawing: 1.8"
    h_15: str = "Walking 2mph (3.2kmh): 2.0"
    h_16: str = "Lifting/packing: 2.1"
    h_17: str = "Seated, heavy limb movement: 2.2"
    h_18: str = "Light machine work: 2.2"
    h_19: str = "Flying aircraft, combat: 2.4"
    h_20: str = "Walking 3mph (4.8kmh): 2.6"
    h_21: str = "House cleaning: 2.7"
    h_22: str = "Driving, heavy vehicle: 3.2"
    h_23: str = "Dancing: 3.4"
    h_24: str = "Calisthenics: 3.5"
    h_25: str = "Walking 4mph (6.4kmh): 3.8"
    h_26: str = "Tennis: 3.8"
    h_27: str = "Heavy machine work: 4.0"
    h_28: str = "Handling 100lb (45 kg) bags: 4.0"


class ModelInputsSelectionClothingPhs(Enum):
    c_1: str = "Walking shorts, short-sleeve shirt: 0.36 clo"
    c_2: str = "Typical summer indoor clothing: 0.5 clo"
    c_3: str = "Knee-length skirt, short-sleeve shirt, sandals, underwear: 0.54 clo"
    c_4: str = "Trousers, short-sleeve shirt, socks, shoes, underwear: 0.57 clo"
    c_5: str = "Trousers, long-sleeve shirt: 0.61 clo"
    c_6: str = "Knee-length skirt, long-sleeve shirt, full slip: 0.67 clo"
    c_7: str = "Sweat pants, long-sleeve sweatshirt: 0.74 clo"
    c_8: str = "Jacket, Trousers, long-sleeve shirt: 0.96 clo"
    c_9: str = "Typical winter indoor clothing: 1.0 clo"


# PMV - EN Chart selection
class ModelInputsSelectionOperativeTemperaturePmvEN16798(Enum):
    o_1: str = "Use operative temp"


# ALL chart description
class ModelChartDescription(Enum):
    note: str = "NOTE:"
    psy_air_temp_des_1: str = (
        "In this psychrometric chart the abscissa is the dry-bulb temperature, and the mean radiant temperature (MRT) is fixed, controlled by the inputbox. Each point on the chart has the same MRT, which defines the comfort zone boundary. In this way you can see how changes in MRT affect thermal comfort. You can also still use the operative temperature button, yet each point will have the same MRT."
    )
    psy_air_temp_des_2: str = (
        "The CBE comfort tools automatically calculates the relative air speed but does not calculates the dynamic insulation characteristics of clothing as specified in the ISO 7730 Section C.2., hence this value should be calculated by the user and entered as input in the CBE comfort tool."
    )
