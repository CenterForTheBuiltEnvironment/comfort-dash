import dash_bootstrap_components as dbc
from dash import dcc, html


def generate_dropdown_inline(
    questions_to_display, value=None, clearable=True, only_dropdown=False
):
    dropdown = dbc.Col(
        dcc.Dropdown(
            options=questions_to_display["options"],
            value=(value if value is not None else questions_to_display["default"]),
            multi=questions_to_display["multi"],
            id=questions_to_display["id"],
            optionHeight=30,
            # todo when possible, avoid using inline styles. Define a global style for the dropdowns
            style={"lineHeight": "1.1rem"},
            clearable=clearable,
        ),
    )
    if only_dropdown:
        return dropdown
    return dbc.Row(
        [
            dbc.Col(
                html.Label(
                    questions_to_display["question"],
                    className="py-2",
                ),
                width="auto",
            ),
            dropdown,
        ],
        className="pb-2",
    )


def generate_dropdown_selection(
    questions_to_display, value=None, clearable=True, only_dropdown=False
):
    dropdown = dbc.Col(
        dcc.Dropdown(
            options=questions_to_display["options"],
            value=(value if value is not None else questions_to_display["default"]),
            multi=questions_to_display["multi"],
            id=questions_to_display["id"],
            optionHeight=30,
            style={"lineHeight": "1.1rem", "fontSize": "14px"},
            clearable=clearable,
        ),
    )
    return dropdown
