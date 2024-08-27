<<<<<<< HEAD
import dash_mantine_components as dmc

from utils.website_text import TextHome


def functionality_selection():
    return dmc.Center(
        [
            dmc.Text(TextHome.functionality_selection.value, mr="sm"),
            dmc.SegmentedControl(
                id="segmented",
                value="ng",
                data=[
                    {"value": "normal", "label": "Single"},
                    {"value": "compare", "label": "Compare"},
                    {"value": "range", "label": "Range"},
                ],
                mb=10,
                radius="lg",
                transitionDuration=500,
            ),
            dmc.Text(id="segmented-value"),
        ]
    )
=======
import dash_mantine_components as dmc

from utils.website_text import TextHome


def functionality_selection():
    return dmc.Center(
        [
            dmc.Text(TextHome.functionality_selection.value, mr="sm"),
            dmc.SegmentedControl(
                id="segmented",
                value="ng",
                data=[
                    {"value": "normal", "label": "Single"},
                    {"value": "compare", "label": "Compare"},
                    {"value": "range", "label": "Range"},
                ],
                mb=10,
                radius="lg",
                transitionDuration=500,
            ),
            dmc.Text(id="segmented-value"),
        ]
    )
>>>>>>> 07f3ad5a1cf463b5e0160290cc18ee3f2914b8e2
