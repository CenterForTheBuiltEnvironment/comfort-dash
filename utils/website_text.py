from enum import Enum

app_name = "CBE Thermal Comfort Tool"


class TextFooter(Enum):
    acknowledgment = "This application has been developed by the Center for the Built Environment and the University of Sydney."


class TextNavBar(Enum):
    home: str = "Home"
    settings: str = "Settings"
    about: str = "About"
    devices: str = "Devices"
