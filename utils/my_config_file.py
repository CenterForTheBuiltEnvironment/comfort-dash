import platform
from enum import Enum
from dataclasses import dataclass
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
    CHART_CONTAINER = "chart-container"
    URL = "url"
    FOOTER = "id-footer"


class Config(Enum):
    # DEBUG: bool = False
    DEBUG: bool = "macOS" in platform.platform()


class URLS(Enum):
    HOME: str = "/"
    ABOUT: str = "/about"


class Stores(Enum):
    INPUT_DATA = "store_input_data"


class MODELS(Enum):
    PMV: str = "PMV - ASHRAE 55"
    Adaptive: str = "Adaptive - ASHRAE 55"
    EN : str = "EN - 16798"



class CHARTS(Enum):
    t_rh: str = "Temperature and Relative Humidity"
    psychrometric: str = "Psychrometric Chart"


class ModelInputsInfo(BaseModel):
    name: str
    unit: str
    min: float
    max: float
    step: float
    value: float


class ModelInputs(BaseModel):
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


class ModelInputs2(BaseModel):
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
        unit="clo", min=0.5, max=2.0, step=0.1, value=0.61, name="Dynamic Clothing insulation"
    )

class ModelInputs3(BaseModel):
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
    # AIR_SPEED: ModelInputsInfo = ModelInputsInfo(
    #
    # )
