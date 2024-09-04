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
    return dbc.Navbar(
        dmc.Grid(
            [
                # Logo Column
                dmc.GridCol(
                    html.A(
                        dbc.Row(
                            dbc.Col(
                                html.Img(
                                    src="/assets/media/CBE-logo-2018.png",
                                    alt="logo website navbar",
                                ),
                            ),
                            align="center",
                        ),
                        href=URLS.HOME.value,
                        style={"textDecoration": "none"},
                    ),
                    span="auto",  # Logo takes up 2 spans
                    className="grid-col-logo justify-content-start",  # Align the logo to the left
                    style={"margin-left": "20px"},
                ),
                dmc.GridCol(
                    html.H1(
                        app_name,
                        id=ElementsIDs.NAVBAR_CONTENT.value,
                        style={
                            "color": "#0c2772",
                            "margin": "0",
                            "fontSize": "32px",
                            "margin-left": "220px",
                            "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
                            "textAlign": "center",  # Center the text within the H1
                            "white-space": "nowrap",  # Ensure the text stays on a single line
                            "width": "100%",  # Ensure the H1 takes up the full width of the column
                        },
                    ),
                    span=2,
                    className="d-flex justify-content-center align-items-center",
                ),
                # Navbar Toggler Column
                dmc.GridCol(
                    dbc.NavbarToggler(
                        dmc.Burger(
                            id=ElementsIDs.NAVBAR_BURGER_BUTTON.value,
                            opened=False,
                            color="black",
                        ),
                        id=ElementsIDs.NAVBAR_TOGGLER.value,
                        n_clicks=0,
                    ),
                    span="auto",
                    className="py-0 grid-toggler",
                ),
                # Navigation Links Column
                dmc.GridCol(
                    dbc.Collapse(
                        dbc.Nav(
                            children=[
                                dbc.NavItem(
                                    dbc.NavLink(
                                        TextNavBar.about.value,
                                        href=URLS.ABOUT.value,
                                        id=ElementsIDs.NAVBAR_ID_ABOUT.value,
                                        style={
                                            "padding": "0 10px",
                                            "margin": "0",
                                            "color": "#3FBBEC",
                                            "paddingTop": "60px",
                                            "fontSize": "16px",
                                            "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
                                        },
                                        className="navbar_right_button",
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.NavLink(
                                        TextNavBar.documentation.value,
                                        href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash",
                                        id=ElementsIDs.NAVBAR_ID_DOCUMENT.value,
                                        style={
                                            "padding": "0 10px",
                                            "margin": "0",
                                            "color": "#3FBBEC",
                                            "paddingTop": "60px",
                                            "fontSize": "16px",
                                            "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
                                        },
                                        className="navbar_right_button",
                                    ),
                                ),
                                dbc.DropdownMenu(
                                    [
                                        dbc.DropdownMenuItem(
                                            item["name"],
                                            href=item["href"],
                                            style={"color": "#0077c2"},
                                        )
                                        for item in tool_items
                                    ],
                                    label=TextNavBar.more_tools.value,
                                    align_end=True,
                                    toggle_style={
                                        "background": "transparent",
                                        "color": "#3FBBEC",
                                        "borderWidth": "0px",
                                        "marginTop": "-5px",
                                        "borderStyle": "none",
                                        "fontSize": "16px",
                                        "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
                                    },
                                    id=ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value,
                                    style={"paddingTop": "60px"},
                                    className="navbar_right_button",
                                ),
                            ],
                            style={
                                "width": "100%",
                                "gap": "20px",
                                "justify-content": "flex-end",
                            },
                        ),
                        id=ElementsIDs.NAVBAR_COLLAPSE.value,
                        is_open=False,
                        navbar=True,
                    ),
                    span="auto",
                    className="py-0 button-right",
                ),
            ],
            justify="space-between",
            align="center",
            className="w-100",
        ),
        color="#fafafa",
        dark=True,
        style={"border-bottom": "1px solid #aeb0ae", "padding": "12px"},
        id=ElementsIDs.NAVBAR.value,
    )


def my_navbar_only_logo():
    return dbc.Navbar(
        dmc.Center(
            html.Img(
                src="assets/media/CBE-logo-2019-artwork-blue-background.png",
                height="30px",
                width="auto",
                alt="logo website navbar",
            ),
        ),
        color="dark",
        dark=True,
        id=ElementsIDs.NAVBAR.value,
    )


# add callback for toggling the collapse on small screens
@callback(
    [
        Output(ElementsIDs.NAVBAR_COLLAPSE.value, "is_open"),
        Output(ElementsIDs.NAVBAR_BURGER_BUTTON.value, "opened"),
        Output(ElementsIDs.NAVBAR_ID_ABOUT.value, "style"),
        Output(ElementsIDs.NAVBAR_ID_DOCUMENT.value, "style"),
        Output(ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value, "style"),
        Output(ElementsIDs.NAVBAR_CONTENT.value, "style"),
    ],
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

    # Set default style with padding-top 60px
    default_style = {
        "paddingTop": "60px",
        "padding": "0 10px",
        "margin": "0",
        "color": "#3FBBEC",
        "fontSize": "16px",
        "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
    }

    # Set toggle style with padding-top 0px
    toggle_style = {
        "paddingTop": "0px",
        "padding": "0 10px",
        "paddingBottom": "10px",
        "margin": "0",
        "color": "#3FBBEC",
        "fontSize": "16px",
        "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
    }

    # Adjust dropdown menu separately with a margin-left
    dropdown_toggle_style = {
        "paddingTop": "0px",
        "padding": "0 10px",
        "paddingBottom": "10px",
        "margin": "0",
        "color": "#3FBBEC",
        "fontSize": "16px",
        "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
        "margin-left": "-10px",
        "background": "transparent",
    }

    # Set default and toggle styles for H1 element
    h1_default_style = {
        "color": "#0c2772",
        "margin": "0",
        "fontSize": "32px",
        "margin-left": "250px",
        "fontFamily": "Open Sans, Arial, Helvetica, sans-serif",
        "textAlign": "center",
        "white-space": "nowrap",
        "width": "100%",
        "display": "block",
    }

    h1_hidden_style = {
        **h1_default_style,
        "display": "none",
    }

    if trigger == ElementsIDs.NAVBAR_TOGGLER.value:
        # Toggle collapse state and adjust padding-top
        new_is_open = not is_open
        new_burger_state = not burger_state

        # Apply different styles for about, documentation, and dropdown menu
        return (
            new_is_open,
            new_burger_state,
            toggle_style if new_is_open else default_style,
            toggle_style if new_is_open else default_style,
            dropdown_toggle_style if new_is_open else default_style,
            h1_hidden_style if not new_burger_state else h1_default_style,
        )

    elif trigger in [
        ElementsIDs.NAVBAR_ID_ABOUT.value,
        ElementsIDs.NAVBAR_ID_DOCUMENT.value,
        ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value,
    ]:
        # Close the collapse when a NavLink is clicked and reset padding-top
        return False, False, default_style, default_style, default_style

    return (
        is_open,
        burger_state,
        default_style,
        default_style,
        default_style,
        h1_default_style,
    )
