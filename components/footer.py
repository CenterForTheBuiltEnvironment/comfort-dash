from dash import html
import dash_mantine_components as dmc

from utils.website_text import TextFooter


def my_footer():
    return html.Div(
        children=[
            html.Footer(
                className="cbe-footer-content",
                children=[
                    # todo do not use html divs but use dash mantine components: ???
                    dmc.Group(
                        className="cbe-footer-logo",
                        children=[
                            dmc.Image(
                                src="assets/media/CBE-logo-2019-white.png",
                                alt="CBE Logo",
                            ),
                            dmc.Image(
                                src="assets/media/ucb-logo-2024-white.png",
                                alt="UC Berkeley Logo",
                            ),
                        ],
                    ),
                    # todo do not use html Nav in the footer, use dash mantine components: done
                    dmc.Group(
                        # todo we should not change the appearance of the logo using css, we should use dash mantine components ???
                        className="cbe-footer-links",
                        children=[
                            dmc.Anchor(
                                "Contact Us",
                                href=TextFooter.contact_us_link.value,
                                target="_blank",
                            ),
                            dmc.Anchor(
                                "Report Issues",
                                href=TextFooter.report_issues_link.value,
                                target="_blank",
                            ),
                        ],
                    ),
                    dmc.Group(
                        className="cbe-social-links",
                        children=[
                            dmc.Anchor(
                                dmc.Image(
                                    src="assets/media/github-white-transparent.png",
                                    alt="GitHub",
                                ),
                                href="#",
                            ),
                            dmc.Anchor(
                                dmc.Image(
                                    src="assets/media/linkedin-white.png",
                                    alt="LinkedIn",
                                ),
                                href="#",
                            ),
                        ],
                        # todo do not use style, use dash mantine components: ???
                    ),
                    dmc.Group(
                        className="cbe-citation-info",
                        children=[
                            dmc.Text(
                                [
                                    dmc.Text(TextFooter.cite_strong.value, fw=700,fz="14px"),
                                    dmc.Text(TextFooter.cite.value,fz="13px"),
                                    dmc.Anchor(
                                        TextFooter.cite_link.value,
                                        href=TextFooter.cite_link.value,
                                        className="cbe-doi-link",
                                        target="_blank",
                                        fz="13px",
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
            dmc.Group(
                className="cbe-footnotes",
                children=[
                    dmc.Text(TextFooter.copy_right.value, fz="11px"),
                    dmc.Group(
                        className="cbe-version-license",
                        children=[
                            dmc.Text(TextFooter.version.value,fz="11px"),
                            dmc.Anchor(
                                dmc.Image(
                                    src="https://img.shields.io/badge/License-MIT-yellow.svg",
                                    alt="License: MIT",
                                    style={"width": "65px", "height": "18px"},
                                ),
                                href=TextFooter.open_source_link.value,
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
