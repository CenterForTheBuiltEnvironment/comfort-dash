import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Input, Output, State, html, ctx
from dash import callback

from utils.my_config_file import URLS, ElementsIDs, Dimensions
from utils.website_text import TextNavBar


def my_navbar():
    return html.Div(
        dbc.Navbar(
            dmc.Container(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            [
                                html.A(
                                    # Use row and col to control vertical alignment of logo / brand
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src="/assets/media/CBE-logo-2018.png",
                                                    height="30px",
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
                            span="content",
                            className="py-0",
                        ),
                        dmc.GridCol(
                            [
                                dbc.NavbarToggler(
                                    dmc.Burger(
                                        id=ElementsIDs.NAVBAR_BURGER_BUTTON.value,
                                        opened=False,
                                        color="white",
                                    ),
                                    id=ElementsIDs.NAVBAR_TOGGLER.value,
                                    n_clicks=0,
                                )
                            ],
                            span="content",
                            className="py-0",
                        ),
                        dmc.GridCol(
                            [
                                dbc.Collapse(
                                    dbc.Nav(
                                        children=[
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    TextNavBar.home.value,
                                                    href=URLS.HOME.value,
                                                    style={"textAlign": "center"},
                                                    id=ElementsIDs.NAVBAR_ID_HOME.value,
                                                ),
                                            ),
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    TextNavBar.about.value,
                                                    href=URLS.ABOUT.value,
                                                    style={"textAlign": "center"},
                                                    id=ElementsIDs.NAVBAR_ID_ABOUT.value,
                                                )
                                            ),
                                        ],
                                    ),
                                    id=ElementsIDs.NAVBAR_COLLAPSE.value,
                                    is_open=False,
                                    navbar=True,
                                ),
                            ],
                            span={"base": 12, "md": 6, "lg": 3},
                            className="py-0",
                        ),
                    ],
                    justify="space-between",
                    align="center",
                ),
                style={"flex": 1},
                className="p-2",
                size=Dimensions.default_container_width.value,
            ),
            color="dark",
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
                        src="/assets/media/CBE-logo-2018.png",
                        height="30px",
                        width="auto",
                        alt="logo website navbar",
                    ),
                ),
                style={"flex": 1},
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
        Input(ElementsIDs.NAVBAR_ID_HOME.value, "n_clicks"),
        # Input(ElementsIDs.NAVBAR_ID_SETTINGS.value, "n_clicks"),
        # Input(ElementsIDs.NAVBAR_ID_ABOUT.value, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def toggle_navbar_collapse(is_open, burger_state, *args):
    trigger = ctx.triggered_id
    if trigger == ElementsIDs.NAVBAR_TOGGLER.value:
        return not is_open, burger_state
    elif is_open:
        return False, not burger_state
    return is_open, burger_state
