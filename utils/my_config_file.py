import platform
from enum import Enum


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
