from enum import Enum

app_name = "CBE Thermal Comfort Tool"


class TextFooter(Enum):
    acknowledgment = "This application has been developed by the Center for the Built Environment and the University of Sydney."
    copy_right  = "Copyright © 2024 The Center for the Built Environment and UC Regents. All right reserved. " 
    cite = "Tartarini, F., Schiavon, S., Cheung, T., Hoyt, T., 2020. CBE Thermal Comfort Tool : online tool for thermal comfort calculations and visualizations. SoftwareX 12, 100563. "
    cite_link = "https://doi.org/10.1016/j.softx.2020.100563."
    contact_us = "Contact us"
    report_issues = "Report issues"
    see_changelog = "See Changelog"
    version = "Version.X.Y.Z"


class TextNavBar(Enum):
    home: str = "Home"
    settings: str = "Settings"
    about: str = "About"
    devices: str = "Devices"


class TextHome(Enum):
    model_selection = "Select model:"
    functionality_selection = "Select functionality:"
    chart_selection = "Select chart:"
    speed_selection = "Speed:"
