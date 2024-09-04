from enum import Enum

app_name = "CBE Thermal Comfort Tool"


class TextFooter(Enum):
    acknowledgment = "This application has been developed by the Center for the Built Environment and the University of Sydney."
    copy_right = "Copyright © 2024 The Center for the Built Environment and UC Regents. All right reserved. "
    cite_strong = "Please cite us if you use this software: "
    cite = "Tartarini, F., Schiavon, S., Cheung, T., Hoyt, T., 2020. CBE Thermal Comfort Tool: online tool for thermal comfort calculations and visualizations. SoftwareX 12, 100563. "
    cite_link = "https://doi.org/10.1016/j.softx.2020.100563"
    contact_us = "Contact us"
    contact_us_link = "https://cbe.berkeley.edu/about-us/contact/"
    report_issues = "Report issues"
    report_issues_link = "https://github.com/CenterForTheBuiltEnvironment/cbe-tool-template/issues/new?labels=bug&template=issue--bug-report.md"
    github_link = "https://github.com/CenterForTheBuiltEnvironment/comfort-dash"
    see_changelog = "See Changelog"
    version = "Version.X.YY"
    open_source_link: str = "https://opensource.org/licenses/MIT"


class TextNavBar(Enum):
    home: str = "Home"
    settings: str = "Settings"
    about: str = "About"
    devices: str = "Devices"
    documentation: str = "Documentation"
    # todo do not call toolsX but call them by their name, see example below
    more_tools: str = "More CBE Tools"
    tool1: str = "CBE Thermal Comfort Tool"
    tool2: str = "CBE Clima Tool"
    tool3: str = "Advanced Ceiling Fan Design Tool"
    tool4: str = "Guidebook on Fans for Cooling People"
    tool5: str = "Occupant Survey Toolkit"
    tool6: str = "CBE Rad Tool"
    tool7: str = "Setpoint Energy Savings Calculator"
    tool8: str = "CBE 3D Mean Radiant Temperature Tool"
    tool9: str = "CBE Underfloor Air Distribution (UFAD) Design Tool"
    tool10: str = "Global Comfort Data Visualization Tools"
    tool11: str = "Python Thermal Comfort Tool: pythermalcomfort"
    tool12: str = "Energy Modeling of Underfloor Air Distribution (UFAD) Systems"


class TextHome(Enum):
    model_selection = "Model:"
    functionality_selection = "Select functionality:"
    chart_selection = "Select chart:"
    speed_selection = "Speed:"
