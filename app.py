import os

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, dcc, html
from icecream import install, ic

from components.footer import my_footer
from components.navbar import my_navbar
from utils.my_config_file import (
    Config,
    MyStores,
    ElementsIDs,
    Dimensions,
)
from utils.website_text import app_name

install()
# from components.dropdowns import Ash55_air_speed_selection
ic.configureOutput(includeContext=True)

# This is required by dash mantine components to work with react 18
dash._dash_renderer._set_react_version("18.2.0")

# Exposing the Flask Server to enable configuring it for logging in
app = Dash(
    __name__,
    title=app_name,
    update_title="Loading...",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap",
        # dash mantine stylesheets
        "https://unpkg.com/@mantine/dates@7/styles.css",
        "https://unpkg.com/@mantine/code-highlight@7/styles.css",
        "https://unpkg.com/@mantine/charts@7/styles.css",
        "https://unpkg.com/@mantine/carousel@7/styles.css",
        "https://unpkg.com/@mantine/notifications@7/styles.css",
        "https://unpkg.com/@mantine/nprogress@7/styles.css",
    ],
    external_scripts=["https://cdn.plot.ly/plotly-basic-2.26.2.min.js"],
    prevent_initial_callbacks=True,
    use_pages=True,
    serve_locally=False,
)
app.config.suppress_callback_exceptions = True

app.layout = dmc.MantineProvider(
    defaultColorScheme="light",
    theme={
        "colorScheme": "dark",
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    children=html.Div(
        [
            my_navbar(),
            dcc.Location(id=ElementsIDs.URL.value),
            dcc.Store(id=MyStores.input_data.value, storage_type="local"),
            html.Div(
                dmc.Container(
                    dash.page_container,
                    p="xs",
                    size=Dimensions.default_container_width.value,
                ),
            ),
            my_footer(),
        ],
        style={
            "minHeight": "100vh",
            "position": "relative",
        },
    ),
)


if __name__ == "__main__":
    app.run_server(
        debug=Config.DEBUG.value,
        host="127.0.0.1",
        port=os.environ.get("PORT_APP", 9090),
        processes=1,
        threaded=True,
    )
