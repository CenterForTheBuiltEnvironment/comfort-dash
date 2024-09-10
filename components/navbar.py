import dash_bootstrap_components as dbc
from dash import html
from utils.my_config_file import URLS, ElementsIDs, ToolUrls
from utils.website_text import TextNavBar, app_name

tool_items = [
    {
        "name": TextNavBar.climaTool.value,
        "href": ToolUrls.clima_tool.value,
    },
    {
        "name": TextNavBar.comfortTool.value,
        "href": ToolUrls.cbe_thermal_comfort_tool.value,
    },
    {
        "name": TextNavBar.fanTool.value,
        "href": ToolUrls.advance_ceiling_fan_design_tool.value,
    },
    {
        "name": TextNavBar.pythermalcomfort.value,
        "href": ToolUrls.python_package_for_thermal_comfort_tool.value,
    },
]


def my_navbar():
    return dbc.Navbar(
        # Container is the navbar itself
        dbc.Container(
            [
                # Use the row is for arrange the position of the LOGO, Title and button
                dbc.Row(
                    [
                        # Use the Col to contain A tag for LOGO
                        dbc.Col(
                            # Make the LOGO can navigate to other website
                            html.A(
                                dbc.Col(
                                    html.Img(
                                        src="assets/media/logo-placeholder.png",
                                        height="80px",
                                    ),
                                ),
                                href=URLS.HOME.value,
                            ),
                            className="mx-auto",
                            width="auto",
                        ),
                        # The title
                        dbc.Col(
                            html.H1(
                                app_name,
                                className="text-center mb-0",
                                style={"color": "#0c2772", "white-space": "nowrap"},
                            ),
                            className="flex-grow-1",
                        ),
                        # three button
                        dbc.Col(
                            dbc.Row(
                                [
                                    # About
                                    dbc.Col(
                                        dbc.Button(
                                            # Make the button's background color to transparent and font color to blue
                                            TextNavBar.about.value,
                                            color="transparent",
                                            className="ms-2",
                                            style={"color": "#3FBBEC"},
                                            id=ElementsIDs.NAVBAR_ID_ABOUT.value,
                                        ),
                                    ),
                                    # Documentation
                                    dbc.Col(
                                        dbc.Button(
                                            # Make the button's background color to transparent and font color to blue
                                            TextNavBar.documentation.value,
                                            color="transparent",
                                            className="ms-2",
                                            style={"color": "#3FBBEC"},
                                            id=ElementsIDs.NAVBAR_ID_DOCUMENT.value,
                                        ),
                                    ),
                                    # More CBE Tools
                                    dbc.DropdownMenu(
                                        [
                                            # Drop down box's item, can found it on the top of the tool_items
                                            dbc.DropdownMenuItem(
                                                item["name"],
                                                href=item["href"],
                                                style={"color": "#0077c2"},
                                            )
                                            for item in tool_items
                                        ],
                                        label=TextNavBar.more_tools.value,
                                        toggle_style={
                                            "background": "transparent",
                                            "color": "#3FBBEC",
                                            "borderStyle": "none",  # no border around the dropdown box
                                        },
                                        id=ElementsIDs.NAVBAR_ID_MORE_CBE_TOOLS.value,
                                    ),
                                ],
                                className="g-0 ms-auto flex-nowrap",
                            ),
                            width="auto",
                        ),
                    ],
                    className="w-100 align-items-center",
                ),
            ],
            fluid=True,
        ),
        color="#F1F3F5",
        dark=True,
        id=ElementsIDs.NAVBAR.value,
    )
