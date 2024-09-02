import dash
import dash_mantine_components as dmc

from components.charts import chart_example
from components.functionality_selection import functionality_selection
from components.input_environmental_personal import input_environmental_personal
from components.dropdowns import (
    model_selection,
    chart_selection,
)
from components.my_card import my_card
from utils.my_config_file import (
    URLS,
    ElementsIDs,
    ModelChartDescription,
    Dimensions,
)
from dash import html, dcc

dash.register_page(__name__, path=URLS.HOME.value)

layout = dmc.Stack(
    [
        dmc.Grid(
            children=[
                dmc.GridCol(
                    model_selection(),
                    # todo we should define the size of the left columns and of the right columns and then create a class and import from there, we should not define them here in the text, see example below
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                dmc.GridCol(
                    functionality_selection(),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
        dmc.Grid(
            children=[
                my_card(
                    title="Inputs",
                    children=input_environmental_personal(),
                    id="input_card",
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                my_card(
                    title="Results and Visualization",
                    children=dmc.Stack(
                        [
                            html.Div(
                                # todo never pass empty string to functions. Define the default values in the function definition
                                id="chart-select",
                                children=chart_selection("", ""),
                            ),
                            dmc.SimpleGrid(
                                cols=3,
                                spacing="xs",
                                verticalSpacing="xs",
                                id="graph-container",
                                children=[
                                    dmc.Center(
                                        dmc.Text("PMV = -0.16"),
                                    ),
                                    dmc.Center(
                                        dmc.Text("PPD = 6 %"),
                                    ),
                                    dmc.Center(
                                        dmc.Text("Sensation = Neutral"),
                                    ),
                                    dmc.Center(
                                        dmc.Text("SET = 24.8 °C"),
                                    ),
                                ],
                                style={"fontSize": "14px"},
                            ),
                            dcc.Graph(
                                id=ElementsIDs.CHART_CONTAINER.value,
                                figure=chart_example("", ""),
                            ),
                            dmc.GridCol(
                                children=dmc.Text(
                                    [
                                        html.Strong(ModelChartDescription.note.value),
                                        ModelChartDescription.psy_air_temp_des_1.value,
                                        dmc.Space(h=20),
                                        ModelChartDescription.psy_air_temp_des_2.value,
                                    ],
                                    style={"fontSize": "14px"},
                                ),
                            ),
                        ],
                    ),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
    ]
)
