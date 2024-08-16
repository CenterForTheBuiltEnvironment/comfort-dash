import dash_mantine_components as dmc
from dash import html

from utils.my_config_file import Dimensions, ElementsIDs
from utils.website_text import TextFooter


def my_footer():
    return html.Div(
        html.Footer(
            dmc.Container(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            dmc.Text(TextFooter.acknowledgment.value),
                            span=8,
                        ),
                        dmc.GridCol(
                            dmc.Image(
                                src="/assets/media/CBE-logo-2018.png",
                                maw=50,
                                mt="md",
                                mb="md",
                                alt="logo",
                            ),
                            span="content",
                        ),
                    ],
                    justify="space-between",
                ),
                p="md",
                size=Dimensions.default_container_width.value,
            ),
            style={
                "background": "#E64626",
                "position": "absolute",
                "bottom": 0,
                "width": "100%",
                "height": "6rem",
            },
        ),
        id=ElementsIDs.FOOTER.value,
    )
