import platform
from enum import Enum
from pydantic import BaseModel


class Dimensions(Enum):
    default_container_width = "md"


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
    SPEED_SELECTION = "id-speed-selection"
    CHART_CONTAINER = "chart-container"
    URL = "url"
    FOOTER = "id-footer"
    NAVBAR_ID_DOCUMENT = "id-nav-documentation"
    NAVBAR_ID_MORE_CBE_TOOLS = "id-nav-more-cbe-tools"


class Config(Enum):
    # DEBUG: bool = False
    DEBUG: bool = "macOS" in platform.platform() or "Windows" in platform.platform()


class URLS(Enum):
    HOME: str = "/"
    ABOUT: str = "/about"
    Documentation: str = "/documentation"
    Tools: str = "/moreCBETools"


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
    Adaptive_ashrae: str = "Adaptive - ASHRAE 55"
    Adaptive_EN: str = "Adaptive - EN 16798"


class CHARTS(Enum):
    t_rh: str = "Temperature and Relative Humidity"
    psychrometric: str = "Psychrometric(air temperature)"
    Psychrometric_operative: str = "Psychrometric(opeative tempeature)"
    Relative_humidity: str = "Relative humidity vs. air temperature"
    Air_speed: str = "Air speed vs. operative temperature"
    Thermal_heat: str = "Thermal heat losses vs. air temperature"
    Set_outputs: str = "SET outputs chart"


class ModelInputsInfo(BaseModel):
    name: str
    unit: str
    min: float
    max: float
    step: float
    value: float


class SPEEDS(Enum):
    s_1: str = "0.3 m/s (59fpm)"
    s_2: str = "0.6 m/s (118fpm)"
    S_3: str = "0.9 m/s (177fpm)"
    s_4: str = "1.2 m/s (236fpm)"


class ModelInputsPmvAshrae55(BaseModel):
    TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=10.0, max=40.0, step=0.1, value=25.0, name="Temperature"
    )
    RH: ModelInputsInfo = ModelInputsInfo(
        unit="%", min=0.0, max=100.0, step=1.0, value=50.0, name="Relative Humidity"
    )
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=1.0, step=0.1, value=0.1, name="Air Speed"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=10.0,
        max=40.0,
        step=0.1,
        value=25.0,
        name="Mean Radiant Temperature",
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=0.7, max=2.0, step=0.1, value=1.2, name="Metabolic Rate"
    )
    CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo", min=0.5, max=2.0, step=0.1, value=0.5, name="Clothing"
    )
    # ACTIVITY: ModelInputsInfo = ModelInputsInfo(
    #     unit="met", min=0.0, max=10.0, step=0.1, value=1.0, name="Activity"
    # )


class ModelInputsAdaptiveEN16798(BaseModel):
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=10.0, max=40.0, step=0.1, value=25.0, name="Air Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=10.0,
        max=40.0,
        step=0.1,
        value=25.0,
        name="Mean Radiant Temperature",
    )
    AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
        unit="m/s", min=0.0, max=1.0, step=0.1, value=0.1, name="Air Speed"
    )
    RH: ModelInputsInfo = ModelInputsInfo(
        unit="%", min=0.0, max=100.0, step=1.0, value=50.0, name="Relative Humidity"
    )
    MET: ModelInputsInfo = ModelInputsInfo(
        unit="met", min=0.7, max=2.0, step=0.1, value=1, name="Metabolic Rate"
    )
    DYNAMIC_CLOTHING: ModelInputsInfo = ModelInputsInfo(
        unit="clo",
        min=0.5,
        max=2.0,
        step=0.1,
        value=0.61,
        name="Dynamic Clothing insulation",
    )


class ModelInputsAdaptiveAshrae55(BaseModel):
    AIR_TEMPERATURE: ModelInputsInfo = ModelInputsInfo(
        unit="°C", min=10.0, max=40.0, step=0.1, value=25.0, name="Temperature"
    )
    MRT: ModelInputsInfo = ModelInputsInfo(
        unit="°C",
        min=10.0,
        max=40.0,
        step=0.1,
        value=25.0,
        name="Prevailing mean outdoor temperature",
    )
