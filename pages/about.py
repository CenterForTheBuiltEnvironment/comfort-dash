<<<<<<< HEAD
import dash
from dash import html

from utils.my_config_file import (
    URLS,
)

dash.register_page(__name__, path=URLS.ABOUT.value)


layout = html.Div(
    "About page",
)
=======
import dash
from dash import html

from utils.my_config_file import (
    URLS,
)

dash.register_page(__name__, path=URLS.ABOUT.value)


layout = html.Div(
    "About page",
)
>>>>>>> 07f3ad5a1cf463b5e0160290cc18ee3f2914b8e2
