import dash_mantine_components as dmc

from utils.my_config_file import Functionalities, ElementsIDs
from utils.website_text import TextHome


def functionality_selection():
    return dmc.Center(
        [
            dmc.Text(TextHome.functionality_selection.value, mr="sm"),
            dmc.SegmentedControl(
                value=Functionalities.Default.value,
                data=[
                    {
                        "value": Functionalities.Default.value,
                        "label": Functionalities.Default.value,
                    },
                    {
                        "value": Functionalities.Compare.value,
                        "label": Functionalities.Compare.value,
                    },
                    {
                        "value": Functionalities.Ranges.value,
                        "label": Functionalities.Ranges.value,
                    },
                ],
                mb=10,
                radius="lg",
                transitionDuration=500,
                id=ElementsIDs.functionality_selection.value,
            ),
        ]
    )
