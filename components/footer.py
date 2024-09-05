import dash_mantine_components as dmc
from utils.website_text import TextFooter

def my_footer():
    return dmc.Group(
        children=[
            dmc.Grid(
                children=[
                dmc.GridCol(
                    dmc.Image(
                        src="/assets/media/CBE-logo-2019-white.png",
                        maw=150,
                        mt=20,
                        ml=10,
                        alt="logo",
                    ),
                    span={"base": 12, "md": 2},
                ),
                dmc.GridCol(
                    dmc.Image(
                        src="/assets/media/ucb-logo-2024-white.png",
                        maw=180,
                        mt=20,
                        ml=-50,
                        alt="berkeley_logo",
                    ),
                    span={"base": 12, "md": 2},
                ),
                dmc.GridCol(
                    dmc.Anchor(
                        dmc.Text(
                            TextFooter.contact_us.value,
                            c="white",
                            size="sm",
                            mt=10,
                            ml=-20,
                        ),
                        href=TextFooter.contact_us_link.value,
                    ),
                    span={"base": 12, "md": 1},
                ),
                dmc.GridCol(
                    dmc.Anchor(
                        dmc.Text(
                            TextFooter.report_issues.value,
                            c="white",
                            size="sm",
                            mt=10,
                            ml=-20,
                        ),
                        href=TextFooter.report_issues_link.value,
                    ),
                    span={"base": 12, "md": 1},
                ),
                dmc.GridCol(
                    dmc.Anchor(
                        dmc.Image(
                            src="/assets/media/github-white-transparent.png",
                            maw=45,
                            ml=60,
                            alt="github logo",
                        ),
                        href="#"
                    ),
                    span={"base": 12, "md": 1},
                ),
                dmc.GridCol(
                    dmc.Anchor(
                        dmc.Image(
                            src="/assets/media/linkedin-white.png",
                            maw=45,
                            ml=35,
                            alt="linkedin logo",
                        ),
                        href="#"
                    ),
                    span={"base": 12, "md": 1},
                ),
                dmc.GridCol(
                    children=[
                        dmc.Text(
                            TextFooter.cite_strong.value,
                            fw=700,
                            c="white",
                            size="sm",
                            mt=20,
                            ml=45,
                        ),
                        dmc.Text(
                            TextFooter.cite.value,
                            c="white",
                            size="sm",
                            ml=45,
                            mr=10,
                        ),
                        dmc.Anchor(
                            dmc.Text(
                                TextFooter.cite_link.value,
                                c="white",
                                size="sm",
                                ml=45,
                                td="underline",
                            ),
                            href=TextFooter.cite_link.value,
                        ),
                    ],
                    span={"base": 12, "md": 4},
                    ),
                ],
                align="center",
                bg="#0077c2",
                w="100%",
                h=150,
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Text(
                            TextFooter.copy_right.value,
                            c="white",
                            size="xs",
                            mt=10,
                            ml=10,
                        ),
                        span={"base": 12, "md": 10, "xs": 10},
                    ),
                    dmc.GridCol(
                        dmc.Text(
                            TextFooter.version.value,
                            c="white",
                            size="xs",
                            mt=10,
                            ml=70,
                        ),
                        ml="none",
                        span={"base": 12, "md": 1, "xs": 1},
                    ),
                    dmc.GridCol(
                        dmc.Anchor(
                            dmc.Image(
                                src="/assets/License-MIT-yellow.svg",
                                maw=70,
                                mt=10,
                                ml=30,
                                alt="license mit logo",
                            ),
                            href=TextFooter.open_source_link.value,
                        ),
                        span={"base": 12, "md": 1, "xs": 1},
                    ),
                ],
                align="center",
                bg="#0c2772",
                w="100%",
                h=40,
            ),
        ],
        gap=0,
        w="100%"
    )