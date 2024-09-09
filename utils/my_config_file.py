import platform
from enum import Enum
from typing import List

from pydantic import BaseModel


class Dimensions(Enum):
    default_container_width = "md"
    left_container_width = 4
    right_container_width = (
        12 - 4
    )  # the sum of the left and right container width should be 12


class ElementsIDs(Enum):
    NAVBAR = "id-navbar"
    NAVBAR_COLLAPSE = "navbar-collapse"
    NAVBAR_TOGGLER = "navbar-toggle"
    NAVBAR_BURGER_BUTTON = "burger-button"
    NAVBAR_CONTENT = "navbar-content"
    NAVBAR_ID_HOME = "id-nav-home"
    NAVBAR_ID_SETTINGS = "id-nav-settings"
    NAVBAR_ID_ABOUT = "id-nav-about"
    MODEL_SELECTION = "id-model-selection"
    chart_selected = "id-chart-selection"
    charts_dropdown = "id-charts-dropdown"
    CHART_CONTAINER = "id-chart-container"
    URL = "url"
    FOOTER = "id-footer"
    INPUT_SECTION = "id-input-section"
    inputs_form = "id-inputs-form"
    t_db_input = "id-dbt-input"
    t_r_input = "id-tr-input"
    t_rm_input = "id-trm-input"
    v_input = "id-v-input"
    rh_input = "id-rh-input"
    met_input = "id-met-input"
    clo_input = "id-clo-input"
    note_model = "id-model-note"
    modal_custom_ensemble = "id-modal-custom-ensemble"
    modal_custom_ensemble_open = "id-modal-custom-ensemble-open"
    modal_custom_ensemble_close = "id-modal-custom-ensemble-close"
    modal_custom_ensemble_submit = "id-modal-custom-ensemble-submit"
    modal_custom_ensemble_value = "id-modal-custom-ensemble-value"
    RESULTS_SECTION = "id-results-section"
    NAVBAR_ID_DOCUMENT = "id-nav-documentation"
    NAVBAR_ID_MORE_CBE_TOOLS = "id-nav-more-cbe-tools"
    HUMIDITY_SELECTION = "id-humidity-selection"
    CLOTHING_SELECTION = "id-clothing-selection"
    METABOLIC_RATE_SELECTION = "id-metabolic-rate-selection"
    ADAPTIVE_ASHARE_SPEED_SELECTION = "id-adaptive-ashare-speed-selection"
    ADAPTIVE_EN_SPEED_SELECTION = "id-adaptive-en-speed-selection"
    PMV_ASHRAE_SPEED_SELECTION = "id-pmv-ashrae-speed-method"
    UNIT_TOGGLE = "id-unit-toggle"  # FOR IP / SI Unit system switch


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


class MyStores(Enum):
    input_data = "store_input_data"


class ChartsInfo(BaseModel):
    name: str
    id: str
    note_chart: str = None


class Charts(Enum):
    t_rh: ChartsInfo = ChartsInfo(
        name="Temperature vs. Relative Humidity",
        id="id_t_rh_chart",
        note_chart="This chart represents only two variables, dry-bulb temperature and relative humidity. The PMV calculations are still based on all the psychrometric variables, but the visualization becomes easier to understand.",
    )
    psychrometric: ChartsInfo = ChartsInfo(
        name="Psychrometric (air temperature)",
        id="id_psy_t_chart",
        note_chart="In this psychrometric chart the abscissa is the dry-bulb temperature, and the mean radiant temperature (MRT) is fixed, controlled by the inputbox. Each point on the chart has the same MRT, which defines the comfort zone boundary. In this way you can see how changes in MRT affect thermal comfort. You can also still use the operative temperature button, yet each point will have the same MRT.",
    )
    psychrometric_operative: ChartsInfo = ChartsInfo(
        name="Psychrometric (operative temperature)",
        id="id_psy_to_chart",
        note_chart="In this psychrometric chart the abscissa is the operative temperature and for each point dry-bulb temperature equals mean radiant temperature (DBT = MRT). The comfort zone represents the combination of conditions with the same DBT and MRT for which the PMV is between -0.5 and +0.5, according to the standard.",
    )


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


class UnitSystem(Enum):
    IP: str = "IP"
    SI: str = "SI"
    m_s: str = "m/s"
    ft_s: str = "ft/s"
    celsius: str = "°C"
    fahrenheit: str = "°F"


class UnitConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return round(celsius * 9 / 5 + 32)

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return round((fahrenheit - 32) * 5 / 9, 2)

    @staticmethod
    def mps_to_fps(mps):
        return round(mps * 3.28084, 2)

    @staticmethod
    def fps_to_mps(fps):
        return round(fps / 3.28084, 2)

    @staticmethod
    def convert_value(value, from_unit, to_unit):
        if (
            from_unit == UnitSystem.celsius.value
            and to_unit == UnitSystem.fahrenheit.value
        ):
            return UnitConverter.celsius_to_fahrenheit(value)
        elif (
            from_unit == UnitSystem.fahrenheit.value
            and to_unit == UnitSystem.celsius.value
        ):
            return UnitConverter.fahrenheit_to_celsius(value)
        elif from_unit == UnitSystem.m_s.value and to_unit == UnitSystem.ft_s.value:
            return UnitConverter.mps_to_fps(value)
        elif from_unit == UnitSystem.ft_s.value and to_unit == UnitSystem.m_s.value:
            return UnitConverter.fps_to_mps(value)
        return value


def convert_units(model_inputs, to_unit_system):
    for input_info in model_inputs:
        if to_unit_system == UnitSystem.IP.value:
            if input_info.unit == UnitSystem.celsius.value:
                input_info.value = UnitConverter.convert_value(
                    input_info.value,
                    UnitSystem.celsius.value,
                    UnitSystem.fahrenheit.value,
                )
                input_info.min = UnitConverter.convert_value(
                    input_info.min,
                    UnitSystem.celsius.value,
                    UnitSystem.fahrenheit.value,
                )
                input_info.max = UnitConverter.convert_value(
                    input_info.max,
                    UnitSystem.celsius.value,
                    UnitSystem.fahrenheit.value,
                )
                input_info.unit = UnitSystem.fahrenheit.value
            elif input_info.unit == UnitSystem.m_s.value:
                input_info.value = UnitConverter.convert_value(
                    input_info.value, UnitSystem.m_s.value, UnitSystem.ft_s.value
                )
                input_info.min = UnitConverter.convert_value(
                    input_info.min, UnitSystem.m_s.value, UnitSystem.ft_s.value
                )
                input_info.max = UnitConverter.convert_value(
                    input_info.max, UnitSystem.m_s.value, UnitSystem.ft_s.value
                )
                input_info.unit = UnitSystem.ft_s.value
        elif to_unit_system == UnitSystem.SI.value:
            if input_info.unit == UnitSystem.fahrenheit.value:
                input_info.value = UnitConverter.convert_value(
                    input_info.value,
                    UnitSystem.fahrenheit.value,
                    UnitSystem.celsius.value,
                )
                input_info.min = UnitConverter.convert_value(
                    input_info.min,
                    UnitSystem.fahrenheit.value,
                    UnitSystem.celsius.value,
                )
                input_info.max = UnitConverter.convert_value(
                    input_info.max,
                    UnitSystem.fahrenheit.value,
                    UnitSystem.celsius.value,
                )
                input_info.unit = UnitSystem.celsius.value
            elif input_info.unit == UnitSystem.ft_s.value:
                input_info.value = UnitConverter.convert_value(
                    input_info.value, UnitSystem.ft_s.value, UnitSystem.m_s.value
                )
                input_info.min = UnitConverter.convert_value(
                    input_info.min, UnitSystem.ft_s.value, UnitSystem.m_s.value
                )
                input_info.max = UnitConverter.convert_value(
                    input_info.max, UnitSystem.ft_s.value, UnitSystem.m_s.value
                )
                input_info.unit = UnitSystem.m_s.value
    return model_inputs


class ModelInputsInfo(BaseModel):
    name: str
    unit: str
    min: float
    max: float
    step: float
    value: float
    id: str


class ModelsInfo(BaseModel):
    name: str
    description: str
    inputs: List[ModelInputsInfo]
    pythermalcomfort_models: str = None
    note_model: str = None
    charts: List[ChartsInfo] = None


class Models(Enum):
    PMV_ashrae: ModelsInfo = ModelsInfo(
        name="PMV - ASHRAE 55",
        description="PMV - ASHRAE 55",
        note_model="This standard is only applicable to healthy individuals. This standard does not apply to occupants: a) whose clothing insulation exceed 1.5 clo; b) whose clothing is highly impermeable; or c) who are sleeping, reclining in contact with bedding, or able to adjust blankets or bedding. The CBE comfort tools automatically calculates the relative air speed and the dynamic clothing insulation.",
        charts=[
            Charts.t_rh.value,
            Charts.psychrometric.value,
            Charts.psychrometric_operative.value,
        ],
        inputs=[
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=10.0,
                max=40.0,
                step=0.5,
                value=25.0,
                name="Air Temperature",
                id=ElementsIDs.t_db_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=10.0,
                max=40.0,
                step=0.5,
                value=25.0,
                name="Mean Radiant Temperature",
                id=ElementsIDs.t_r_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.m_s.value,
                min=0.0,
                max=2.0,
                step=0.1,
                value=0.1,
                name="Air Speed",
                id=ElementsIDs.v_input.value,
            ),
            ModelInputsInfo(
                unit="%",
                min=0.0,
                max=100.0,
                step=1.0,
                value=50.0,
                name="Relative Humidity",
                id=ElementsIDs.rh_input.value,
            ),
            ModelInputsInfo(
                unit="met",
                min=1,
                max=4.0,
                step=0.1,
                value=1.0,
                name="Metabolic Rate",
                id=ElementsIDs.met_input.value,
            ),
            ModelInputsInfo(
                unit="clo",
                min=0.0,
                max=1.5,
                step=0.1,
                value=0.61,
                name="Clothing Level",
                id=ElementsIDs.clo_input.value,
            ),
        ],
    )
    PMV_EN: ModelsInfo = ModelsInfo(
        name="PMV - EN",
        description="PMV - EN",
        note_model="The CBE comfort tools automatically calculates the relative air speed but does not calculates the dynamic insulation characteristics of clothing as specified in the ISO 7730 Section C.2., hence this value should be calculated by the user and entered as input in the CBE comfort tool.",
        charts=[
            # todo add the right charts
            Charts.psychrometric.value,
            Charts.psychrometric_operative.value,
        ],
        inputs=[
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=10.0,
                max=30.0,
                step=0.5,
                value=25.0,
                name="Air Temperature",
                id=ElementsIDs.t_db_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=10.0,
                max=40.0,
                step=0.5,
                value=25.0,
                name="Mean Radiant Temperature",
                id=ElementsIDs.t_r_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.m_s.value,
                min=0.0,
                max=1.0,
                step=0.1,
                value=0.1,
                name="Air Speed",
                id=ElementsIDs.v_input.value,
            ),
            ModelInputsInfo(
                unit="%",
                min=0.0,
                max=100.0,
                step=1.0,
                value=50.0,
                name="Relative Humidity",
                id=ElementsIDs.rh_input.value,
            ),
            ModelInputsInfo(
                unit="met",
                min=0.8,
                max=4.0,
                step=0.1,
                value=1.0,
                name="Metabolic Rate",
                id=ElementsIDs.met_input.value,
            ),
            ModelInputsInfo(
                unit="clo",
                min=0.0,
                max=2.0,
                step=0.1,
                value=0.61,
                name="Clothing Level",
                id=ElementsIDs.clo_input.value,
            ),
        ],
    )
    Adaptive_ASHRAE: ModelsInfo = ModelsInfo(
        name="Adaptive - ASHRAE 55",
        description="Adaptive - ASHRAE 55",
        charts=[
            # todo add the right charts
            Charts.t_rh.value,
        ],
        inputs=[
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=0.0,
                max=50.0,
                step=0.5,
                value=25.0,
                name="Air Temperature",
                id=ElementsIDs.t_db_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=0.0,
                max=50.0,
                step=0.5,
                value=25.0,
                name="Mean Radiant Temperature",
                id=ElementsIDs.t_r_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.celsius.value,
                min=10.0,
                max=35.0,
                step=0.5,
                value=25.0,
                name="Prevailing mean outdoor temperature",
                id=ElementsIDs.t_rm_input.value,
            ),
            ModelInputsInfo(
                unit=UnitSystem.m_s.value,
                min=0.0,
                max=4.0,
                step=0.1,
                value=0.1,
                name="Air Speed",
                id=ElementsIDs.v_input.value,
            ),
        ],
    )


# PMV - Ashare right selection
class ModelInputsSelectionSpeedASHRAE55(Enum):
    s_1: str = "No local control"
    s_2: str = "with local control"


class ModelInputsSelectionSpeedASHRAE55(Enum):
    s_1: str = "No local control"
    s_2: str = "with local control"


class HumiditySelection(Enum):
    h_1: str = "Relative humidity"
    h_2: str = "Humidity ratio"
    h_3: str = "Dew point"
    h_4: str = "Wet bulb"
    h_5: str = "Vapor pressure"


class MetabolicRateSelection(Enum):
    sleeping: str = "Sleeping: 0.7"
    reclining: str = "Reclining: 0.8"
    # todo change the key names
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


class ClothingSelection(Enum):
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
