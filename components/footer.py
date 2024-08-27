<<<<<<< HEAD
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
                                    maw=130,
                                    mt="none",
                                    mb="none",
                                    ml="20px",
                                    alt="logo",
                                ),
                                span={"base": 12, "md": 2},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/berkeley.png",
                                    maw=130,
                                    mt="5px",
                                    mb="none",
                                    ml="none",
                                    alt="berkeley_logo",
                                ),
                                span={"base": 12, "md": 2.5},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            dmc.GridCol(
                                html.Div(
                                    [
                                        html.A(
                                            dmc.Text(
                                                TextFooter.contact_us.value,
                                                style={
                                                    "color": "white",
                                                    "fontSize": "9px",
                                                },
                                            ),
                                            href=TextFooter.contact_us_link.value,
                                            style={"textDecoration": "none"},
                                        ),
                                        html.A(
                                            dmc.Text(
                                                TextFooter.report_issues.value,
                                                style={
                                                    "color": "white",
                                                    "fontSize": "9px",
                                                },
                                            ),
                                            href=TextFooter.report_issues_link.value,
                                            style={"textDecoration": "none"},
                                        ),
                                        dmc.Text(
                                            TextFooter.see_changelog.value,
                                            style={"color": "white", "fontSize": "9px"},
                                        ),
                                    ],
                                ),
                                mt="3px",
                                span={"base": 12, "xs": 6, "md": 1},
                                ml="5px",
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            dmc.GridCol(
                                html.A(
                                    dmc.Image(
                                        src="/assets/media/github-white-transparent.png",
                                        maw=40,
                                        mt="7px",
                                        mb="none",
                                        alt="logo",
                                    ),
                                    href=TextFooter.github_link.value,
                                ),
                                span={"base": 12, "xs": 6, "md": 1},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            dmc.GridCol(
                                dmc.Image(
                                    src="/assets/media/linkedin-white.png",
                                    maw=40,
                                    mt="7px",
                                    mb="none",
                                    alt="logo",
                                ),
                                span={"base": 12, "xs": 6, "md": 1},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            dmc.GridCol(
                                html.Div(
                                    [
                                        html.A(
                                            dmc.Text(
                                                [
                                                    html.Strong(
                                                        TextFooter.cite_strong.value
                                                    ),
                                                    TextFooter.cite.value,
                                                    html.Span(
                                                        TextFooter.cite_link.value,
                                                        style={
                                                            "textDecoration": "underline"
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "color": "white",
                                                    "fontSize": "9px",
                                                },
                                            ),
                                            href=TextFooter.cite_link.value,
                                            style={"textDecoration": "none"},
                                        )
                                    ],
                                ),
                                span={"base": 12, "xs": 12, "md": 4},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                        ],
                        justify="start",
                        align="start",
                        gutter="md",
                    ),
                    p="0",
                    size=Dimensions.default_container_width.value,
                ),
                style={
                    "background": "#3375BC",
                    "position": "relatived",
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
                                    style={"color": "white", "fontSize": "9px"},
                                ),
                                ml="none",
                                span={"base": 12, "md": 10, "xs": 10},
                            ),
                            dmc.GridCol(
                                dmc.Text(
                                    TextFooter.version.value,
                                    style={"color": "white", "fontSize": "9px"},
                                ),
                                ml="none",
                                span={"base": 12, "md": 1, "xs": 1},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
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
                                span={"base": 12, "md": 1, "xs": 1},
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                        ],
                        justify="space-between",
                        align="center",
                        gutter="md",
                    ),
                    p="0",
                    size=Dimensions.default_container_width.value,
                ),
                style={
                    "background": "#1B3A76",
                    "width": "100%",
                    "min-height": "1rem",
                    "position": "relatived",
                    "bottom": 0,
                },
            ),
        ]
    )
=======
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
>>>>>>> 07f3ad5a1cf463b5e0160290cc18ee3f2914b8e2
