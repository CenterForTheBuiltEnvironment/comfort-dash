import dash_mantine_components as dmc
from dash import html

from utils.my_config_file import Dimensions, ElementsIDs
from utils.website_text import TextFooter


def my_footer():
    return html.Div(
        children=[
            html.Footer(
                dmc.Container(
                    dmc.Grid(
                        [
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/CBE-logo-2019-artwork-blue-background.png",
                                    maw=150,
                                    mt="none",
                                    mb="none",
                                    ml="-10px",
                                    alt="logo",
                                ),
                                span=2,
                            ),
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/berkeley.png",
                                    maw=150,
                                    mt="5px",
                                    mb="none",
                                    ml="none",
                                    alt="logo",
                                ),
                                span=2.5,
                            ),
                            dmc.GridCol(
                                html.Div(
                                    [   html.A(
                                            dmc.Text(
                                                TextFooter.contact_us.value,
                                                style={"color":"white", "fontSize":"9px"}
                                            ),
                                            href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash/discussions",
                                            style={"textDecoration": "none"}
                                        ),
                                        html.A(
                                            dmc.Text(
                                                TextFooter.report_issues.value,
                                                style={"color":"white", "fontSize":"9px"}
                                            ),
                                            href="https://github.com/CenterForTheBuiltEnvironment/comfort-dash/issues",
                                            style={"textDecoration": "none"}
                                        ),
                                        dmc.Text(
                                            TextFooter.see_changelog.value,
                                            style={"color":"white", "fontSize":"9px"}
                                        ),
                                    ],
                                ),
                                mt="3px",
                                span=1.5,
                            ),
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/github-white-transparent.png",
                                    maw=40,
                                    mt="7px",
                                    mb="none",
                                    alt="logo",
                                ),
                                span=1,
                        ),
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/linkedin-white.png",
                                    maw=40,
                                    mt="7px",
                                    mb="none",
                                    alt="logo",
                                ),
                                span=1,
                            ),
                            dmc.GridCol(
                                html.Div(
                                    [
                                        html.A(
                                            dmc.Text(
                                                [
                                                    html.Strong("Please cite us if you use this software: "),
                                                    TextFooter.cite.value,
                                                    html.Span(
                                                        TextFooter.cite_link.value,
                                                        style={"textDecoration":"underline"}
                                                    )
                                                ],
                                                style={"color":"white", "fontSize":"9px"}
                                            ),
                                            href="https://doi.org/10.1016/j.softx.2020.100563",
                                            style={"textDecoration": "none"}

                                        )
                                    ],
                                ),
                                span=4.0,
                            ),
                        ],
                        justify="start",
                        align="start",
                        gutter="md"
                    ),
                    p="0",
                    size=Dimensions.default_container_width.value,
                ),
                style={
                    "background": "#3375BC",
                    "position": "absolute",
                    "bottom": 0,
                    "width": "100%",
                    "min-height": "5rem",

                },
                id=ElementsIDs.FOOTER.value,  
        ),
        html.Footer(
                    dmc.Container(
                        dmc.Grid(
                            [
                                dmc.GridCol(
                                    dmc.Text(
                                        TextFooter.copy_right.value,
                                        style={"color":"white","fontSize":"9px"}
                                    ),
                                    ml="-10px",
                                    span=10,
                                ),
                                dmc.GridCol(
                                    dmc.Text(
                                        TextFooter.version.value, 
                                        style={"color":"white","fontSize":"9px"}
                                    ),
                                    ml="10px",
                                    span=1,
                                ),
                                dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/share.png",
                                    maw=50,
                                    mt="none",
                                    mb="none",
                                    ml="none",
                                    alt="logo",
                                ),
                                span=1,
                            ),
                            ],
                            justify="space-between",
                            align="center",
                            gutter="md"
                        ),
                        p="0",
                        size=Dimensions.default_container_width.value,
                    ),
                    style={
                        "background": "#1B3A76", 
                        "width": "100%",
                        "min-height": "1rem",
                        "position": "fixed",
                        "bottom":0,
                    },
                ),
            ]
        )