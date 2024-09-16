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
    more_tools: str = "More CBE Tools"
    climaTool: str = "CBE Clima Tool"
    comfortTool: str = "CBE Comfort Tool"
    fanTool: str = "CBE Fan Tool"
    pythermalcomfort: str = "pythermalcomfort"


class TextHome(Enum):
    model_selection = "Model:"
    functionality_selection = "Select functionality:"
    chart_selection = "Select chart:"
    speed_selection = "Speed:"


class TextWarning(Enum):
    clo_warning_exceed: str = "Clothing Level cannot exceed "
    clo_warning_less: str = "Clothing Level cnnot less than "
    clo_warning_current_total: str = ". Current total: "
    clo_warning_clo: str = " clo."
