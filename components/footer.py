from dash import html

from utils.website_text import TextFooter


def my_footer():
    return html.Div(
        children=[
            html.Footer(
                className="cbe-footer-content",
                children=[
                    html.Div(
                        className="cbe-footer-logo",
                        children=[
                            html.Img(
                                src="assets/media/CBE-logo-2019-white.png",
                                alt="CBE Logo",
                            ),
                            html.Img(
                                src="assets/media/ucb-logo-2024-white.png",
                                alt="UC Berkeley Logo",
                            ),
                        ],
                    ),
                    html.Nav(
                        className="cbe-footer-links",
                        children=[
                            html.A(
                                "Contact Us",
                                href=TextFooter.contact_us_link.value,
                                target="_blank",
                            ),
                            html.A(
                                "Report Issues",
                                href=TextFooter.report_issues_link.value,
                                target="_blank",
                            ),
                        ],
                        style={"position": "relative", "left": "-9px"},
                    ),
                    html.Nav(
                        className="cbe-social-links",
                        children=[
                            html.A(
                                html.Img(
                                    src="assets/media/github-white-transparent.png",
                                    alt="GitHub",
                                ),
                                href="#",
                            ),
                            html.A(
                                html.Img(
                                    src="assets/media/linkedin-white.png",
                                    alt="LinkedIn",
                                ),
                                href="#",
                            ),
                        ],
                        style={"position": "relative", "left": "-9px"},
                    ),
                    html.Div(
                        className="cbe-citation-info",
                        children=[
                            html.Strong(TextFooter.cite_strong.value),
                            html.Div(
                                [
                                    TextFooter.cite.value,
                                    html.A(
                                        TextFooter.cite_link.value,
                                        href=TextFooter.cite_link.value,
                                        className="cbe-doi-link",
                                        target="_blank",
                                    ),
                                ]
                            ),
                        ],
                        style={"position": "relative", "left": "-9px"},
                    ),
                ],
            ),
            html.Div(
                className="cbe-footnotes",
                style={
                    "background-color": "#1B3A76",
                    "min-height": "2.5rem",
                    "padding": "10px",
                },
                children=[
                    html.Div(
                        TextFooter.copy_right.value,
                    ),
                    html.Div(
                        className="cbe-version-license",
                        children=[
                            html.Div(TextFooter.version.value),
                            html.A(
                                html.Img(
                                    src="https://img.shields.io/badge/License-MIT-yellow.svg",
                                    alt="License: MIT",
                                    style={"width": "70px", "height": "17px"},
                                ),
                                href=TextFooter.open_source_link.value,
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
