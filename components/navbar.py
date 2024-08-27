import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Input, Output, State, html, ctx
from dash import callback

from utils.my_config_file import URLS, ElementsIDs, Dimensions, ToolUrls
from utils.website_text import TextNavBar, app_name


tool_items = [
    {"name": TextNavBar.tool1.value, "href": ToolUrls.cbe_thermal_comfort_tool.value},
    {"name": TextNavBar.tool2.value, "href": ToolUrls.clima_tool.value},
    {
        "name": TextNavBar.tool3.value,
        "href": ToolUrls.advance_ceiling_fan_design_tool.value,
    },
    {
        "name": TextNavBar.tool4.value,
        "href": ToolUrls.guidebook_on_fans_for_cooling_people_tool.value,
    },
    {
        "name": TextNavBar.tool5.value,
        "href": ToolUrls.occupant_survey_and_building_benchmarking_tool.value,
    },
    {
        "name": TextNavBar.tool6.value,
        "href": ToolUrls.cbe_rad_tool_early_design_tool_for_high_thermal_mass_radiant_syste_tool.value,
    },
    {
        "name": TextNavBar.tool7.value,
        "href": ToolUrls.setpoint_energy_savings_calculator_tool.value,
    },
    {
        "name": TextNavBar.tool8.value,
        "href": ToolUrls.cbe_3d_mean_radiant_temperature_tool.value,
    },
    {
        "name": TextNavBar.tool9.value,
        "href": ToolUrls.underfloor_air_distribution_ufad_cooling_load_design_tool.value,
    },
    {
        "name": TextNavBar.tool10.value,
        "href": ToolUrls.global_comfort_data_visualization_tool.value,
    },
    {
        "name": TextNavBar.tool11.value,
        "href": ToolUrls.python_package_for_thermal_comfort_tool.value,
    },
    {
        "name": TextNavBar.tool12.value,
        "href": ToolUrls.energy_performance_modeling_underfloor_air_distribution_systems_tool.value,
    },
]


def my_navbar():
    return html.Div(
        dbc.Navbar(
            html.Div(
                dmc.Grid(
                    [
                        # Logo Column
                        dmc.GridCol(
                            [
                                html.A(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src="/assets/media/CBE-logo-2018.png",
                                                    height="100px",
                                                    width="auto",
                                                    alt="logo website navbar",
                                                ),
                                                width="auto",
                                            ),
                                        ],
                                        align="center",
                                        className="g-0",
                                    ),
                                    href=URLS.HOME.value,
                                    style={"textDecoration": "none"},
                                ),
                            ],
                            span="auto",  # Logo takes up 2 spans
                            className="d-flex justify-content-start",  # Align the logo to the left
                        ),
                        # Center H1 Column
                        dmc.GridCol(
                            [
                                html.H1(
                                    app_name,
                                    style={
                                        "textAlign": "center",
                                        "color": "#0b2672",
                                        "margin": "0",
                                        "width": "100%",
                                        "fontWeight": "bold",
                                        # "lineHeight": "180px",
                                        "paddingBottom": "1px",
                                    },
                                )
                            ],
                            span="auto",
                            className="d-flex justify-content-center align-items-center",
                        ),
                        dmc.GridCol(
                            [
                                dbc.NavbarToggler(
                                    dmc.Burger(
                                        id=ElementsIDs.NAVBAR_BURGER_BUTTON.value,
                                        opened=False,
                                        color="black",
                                    ),
                                    id=ElementsIDs.NAVBAR_TOGGLER.value,
                                    n_clicks=0,
                                )
                            ],
                            span="content",
                            className="py-0",
                        ),
                        # Navigation Links Column
                        dmc.GridCol(
                            [
                                dbc.Collapse(
                                    dbc.Nav(
                                        children=[
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    TextNavBar.about.value,
                                                    href=URLS.ABOUT.value,
                                                    style={
                                                        "padding": "0 10px",
                                                        "margin": "0",
                                                        "color": "#0078c2",
                                                    },
                                                    id=ElementsIDs.NAVBAR_ID_ABOUT.value,
                                                )
                                            ),
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    TextNavBar.documentation.value,
                                                    href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash",
                                                    style={
                                                        "padding": "0 10px",
                                                        "margin": "0",
                                                        "color": "#0078c2",
                                                    },
                                                    id=ElementsIDs.NAVBAR_ID_DOCUMENT.value,
                                                ),
                                            ),
                                            dbc.DropdownMenu(
                                                [
                                                    dbc.DropdownMenuItem(
                                                        item["name"],
                                                        href=item["href"],
                                                        style={
                                                            "padding": "0 10px",
                                                            "margin": "0",
                                                        },
                                                    )
                                                    for item in tool_items
                                                ],
                                                label=TextNavBar.tools.value,
                                                align_end=True,
                                                toggle_style={
                                                    "background": "white",
                                                    "color": "#0078c2",
                                                    "borderColor": "rgba(255,255,255,0.2)",
                                                    "marginTop": "-8px",
                                                },
                                                id=ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value,
                                            ),
                                        ],
                                        # Make the text stick on right
                                        style={
                                            "width": "100%",
                                            "justify-content": "flex-end",
                                        },
                                    ),
                                    id=ElementsIDs.NAVBAR_COLLAPSE.value,
                                    is_open=False,
                                    navbar=True,
                                ),
                            ],
                            span="auto",
                            className="py-0",
                        ),
                    ],
                    justify="space-between",
                    align="center",
                    className="w-100",  # Ensure full width
                ),
                style={"flex": 1},
                className="d-flex justify-content-between align-items-center w-100",  # Flexbox layout for full width
            ),
            color="white",
            dark=True,
        ),
        id=ElementsIDs.NAVBAR.value,
    )


def my_navbar_only_logo():
    return html.Div(
        dbc.Navbar(
            dmc.Container(
                dmc.Center(
                    html.Img(
                        src="assets/media/CBE-logo-2019-artwork-blue-background.png",
                        height="30px",
                        width="auto",
                        alt="logo website navbar",
                    ),
                ),
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "flex-start",
                    "padding": "0",
                    "margin": "0",
                },
                className="p-1",
                size=Dimensions.default_container_width.value,
            ),
            color="dark",
            dark=True,
        ),
        id=ElementsIDs.NAVBAR.value,
    )


# add callback for toggling the collapse on small screens
@callback(
    Output(ElementsIDs.NAVBAR_COLLAPSE.value, "is_open"),
    Output(ElementsIDs.NAVBAR_BURGER_BUTTON.value, "opened"),
    [
        State(ElementsIDs.NAVBAR_COLLAPSE.value, "is_open"),
        State(ElementsIDs.NAVBAR_BURGER_BUTTON.value, "opened"),
    ],
    [
        Input(ElementsIDs.NAVBAR_TOGGLER.value, "n_clicks"),
        Input(ElementsIDs.NAVBAR_ID_ABOUT.value, "n_clicks"),
        Input(ElementsIDs.NAVBAR_ID_DOCUMENT.value, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_navbar_collapse(is_open, burger_state, *args):
    trigger = ctx.triggered_id

    # When the toggler is clicked, toggle the collapse state
    if trigger == ElementsIDs.NAVBAR_TOGGLER.value:
        return not is_open, not burger_state

    # If any of the NavLinks are clicked, close the collapse
    elif trigger in [
        ElementsIDs.NAVBAR_ID_ABOUT.value,
        ElementsIDs.NAVBAR_ID_DOCUMENT.value,
        ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value,
    ]:
        return False, False

    return is_open, burger_state
