import dash
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, State

from utils.my_config_file import (
    ModelInputsInfo,
    Models,
    convert_units,
    ElementsIDs,
    UnitSystem,
    MetabolicRateSelection,
    ClothingSelection,
)
from utils.website_text import (
    TextWarning,
)
import dash
from components.show_results import display_results


def modal_custom_ensemble():
    return dmc.Modal(
        title="Custom Ensemble",
        id=ElementsIDs.modal_custom_ensemble.value,
        zIndex=10000,
        children=[
            dmc.Stack(
                [
                    dmc.Text(
                        "Select all the garments you want to include in the ensemble"
                    ),
                    dmc.MultiSelect(
                        id=ElementsIDs.modal_custom_ensemble_value.value,
                        data=[
                            {
                                "group": "Underwear",
                                "items": [
                                    {"value": "0.01_Bra", "label": "Bra (0.01 clo)"},
                                    {
                                        "value": "0.03",
                                        "label": "Women's underwear (0.03 clo)",
                                    },
                                    {
                                        "value": "0.04",
                                        "label": "Men's underwear (0.04 clo)",
                                    },
                                    {
                                        "value": "0.14_Half_slip",
                                        "label": "Half slip (0.14 clo)",
                                    },
                                    {
                                        "value": "0.15_Long_underwear_bottoms",
                                        "label": "Long underwear bottoms (0.15 clo)",
                                    },
                                    {"value": "0.16", "label": "Full slip (0.16 clo)"},
                                    {
                                        "value": "0.20_Long_underwear",
                                        "label": "Long underwear top (0.2 clo)",
                                    },
                                ],
                            },
                            {
                                "group": "Tops",
                                "items": [
                                    {
                                        "value": "0.08_T_shirt",
                                        "label": "T-shirt (0.08 clo)",
                                    },
                                    {
                                        "value": "0.12",
                                        "label": "Sleeveless scoop-neck blouse (0.12 clo)",
                                    },
                                    {
                                        "value": "0.17",
                                        "label": "Short-sleeve knit shirt (0.17 clo)",
                                    },
                                    {
                                        "value": "0.10_Sleevelss_vest_thin",
                                        "label": "Sleeveless vest (thin) (0.1 clo)",
                                    },
                                    {
                                        "value": "0.17_Sleevelss_vest_thick",
                                        "label": "Sleeveless vest (thick) (0.17 clo)",
                                    },
                                    {
                                        "value": "0.18",
                                        "label": "Sleeveless short gown (thin) (0.18 clo)",
                                    },
                                    {
                                        "value": "0.19",
                                        "label": "Short-sleeve dress shirt (0.19 clo)",
                                    },
                                    {
                                        "value": "0.20_Sleevelss_long_gown_thin",
                                        "label": "Sleeveless long gown (thin) (0.2 clo)",
                                    },
                                    {
                                        "value": "0.25_Long_sleeve_dress_shirt",
                                        "label": "Long-sleeve dress shirt (0.25 clo)",
                                    },
                                    {
                                        "value": "0.34",
                                        "label": "Long-sleeve flannel shirt (0.34 clo)",
                                    },
                                    {
                                        "value": "0.34_Long_sleeve_sweat_shirt",
                                        "label": "Long-sleeve sweat shirt (0.34 clo)",
                                    },
                                    {
                                        "value": "0.31",
                                        "label": "Short-sleeve hospital gown (0.31 clo)",
                                    },
                                    {
                                        "value": "0.34_Short_sleeve_short_robe_thin",
                                        "label": "Short-sleeve short robe (thin) (0.34 clo)",
                                    },
                                    {
                                        "value": "0.42_Short_sleeve_pajamas",
                                        "label": "Short-sleeve pajamas (0.42 clo)",
                                    },
                                    {
                                        "value": "0.46",
                                        "label": "Short-sleeve long gown (0.46 clo)",
                                    },
                                    {
                                        "value": "0.48",
                                        "label": "Short-sleeve short wrap robe (thick) (0.48 clo)",
                                    },
                                    {
                                        "value": "0.57",
                                        "label": "Short-sleeve pajamas (thick) (0.57 clo)",
                                    },
                                    {
                                        "value": "0.69",
                                        "label": "Short-sleeve long wrap robe (thick) (0.69 clo)",
                                    },
                                    {"value": "0.30", "label": "Overalls (0.3 clo)"},
                                    {"value": "0.49", "label": "Coveralls (0.49 clo)"},
                                    {
                                        "value": "0.23",
                                        "label": "Sleeveless, scoop-neck shirt (thin) (0.23 clo)",
                                    },
                                    {
                                        "value": "0.27",
                                        "label": "Sleeveless, scoop-neck shirt (thick) (0.27 clo)",
                                    },
                                    {
                                        "value": "0.13",
                                        "label": "Sleeveless vest (thin) (0.13 clo)",
                                    },
                                    {
                                        "value": "0.22",
                                        "label": "Sleeveless vest (thick) (0.22 clo)",
                                    },
                                    {
                                        "value": "0.25",
                                        "label": "Long sleeve shirt (thin) (0.25 clo)",
                                    },
                                    {
                                        "value": "0.36_Long_sleeve_shirt_thick",
                                        "label": "Long sleeve shirt (thick) (0.36 clo)",
                                    },
                                    {
                                        "value": "0.36",
                                        "label": "Single-breasted coat (thin) (0.36 clo)",
                                    },
                                    {
                                        "value": "0.44",
                                        "label": "Single-breasted coat (thick) (0.44 clo)",
                                    },
                                    {
                                        "value": "0.42",
                                        "label": "Double-breasted coat (thin) (0.42 clo)",
                                    },
                                    {
                                        "value": "0.48_Double_breasted_coat_thick",
                                        "label": "Double-breasted coat (thick) (0.48 clo)",
                                    },
                                ],
                            },
                            {
                                "group": "Trousers",
                                "items": [
                                    {
                                        "value": "0.06_Short_shorts",
                                        "label": "Short shorts (0.06 clo)",
                                    },
                                    {
                                        "value": "0.08",
                                        "label": "Walking shorts (0.08 clo)",
                                    },
                                    {"value": "0.14", "label": "Thin skirt (0.14 clo)"},
                                    {
                                        "value": "0.23_Thick_skirt",
                                        "label": "Thick skirt (0.23 clo)",
                                    },
                                    {
                                        "value": "0.15_Thin_trousers",
                                        "label": "Thin trousers (0.15 clo)",
                                    },
                                    {
                                        "value": "0.24",
                                        "label": "Thick trousers (0.24 clo)",
                                    },
                                    {"value": "0.28", "label": "Sweatpants (0.28 clo)"},
                                    {
                                        "value": "0.33",
                                        "label": "Long-sleeve shirtdress (thin) (0.33 clo)",
                                    },
                                    {
                                        "value": "0.47",
                                        "label": "Long-sleeve shirtdress (thick) (0.47 clo)",
                                    },
                                    {
                                        "value": "0.29",
                                        "label": "Short-sleeve shirtdress (0.29 clo)",
                                    },
                                ],
                            },
                            {
                                "group": "Socks",
                                "items": [
                                    {
                                        "value": "0.02_Ankle_socks",
                                        "label": "Ankle socks (0.02 clo)",
                                    },
                                    {
                                        "value": "0.02_Panty_hose",
                                        "label": "Panty hose (0.02 clo)",
                                    },
                                    {
                                        "value": "0.03_Claf_length_socks",
                                        "label": "Calf length socks (0.03 clo)",
                                    },
                                    {
                                        "value": "0.06",
                                        "label": "Knee socks (thick) (0.06 clo)",
                                    },
                                ],
                            },
                            {
                                "group": "Shoes",
                                "items": [
                                    {
                                        "value": "0.02",
                                        "label": "Shoes or sandals (0.02 clo)",
                                    },
                                    {
                                        "value": "0.03_Slippers",
                                        "label": "Slippers (0.03 clo)",
                                    },
                                    {"value": "0.10_Boots", "label": "Boots (0.1 clo)"},
                                ],
                            },
                            {
                                "group": "Chair",
                                "items": [
                                    {"value": "0.00", "label": "Metal chair (0 clo)"},
                                    {
                                        "value": "0.01",
                                        "label": "Wooden stool (0.01 clo)",
                                    },
                                    {
                                        "value": "0.10",
                                        "label": "Standard office chair (0.1 clo)",
                                    },
                                    {
                                        "value": "0.15",
                                        "label": "Executive chair (0.15 clo)",
                                    },
                                ],
                            },
                        ],
                        styles={"dropdown": {"z-index": "10002"}},
                        # w=400,
                    ),
                    dmc.Alert(
                        dmc.Text("warning message"),
                        id=ElementsIDs.modal_custom_ensemble_warning.value,
                        color="red",
                        withCloseButton=False,
                        display="none",
                    ),
                    dmc.Group(
                        [
                            dmc.Button(
                                "Set Clo value",
                                id=ElementsIDs.modal_custom_ensemble_submit.value,
                            ),
                            dmc.Button(
                                "Close",
                                color="red",
                                variant="outline",
                                id=ElementsIDs.modal_custom_ensemble_close.value,
                            ),
                        ],
                        justify="flex-end",
                    ),
                ]
            )
        ],
    )


def input_environmental_personal(
    selected_model: str = "PMV_ashrae",
    units: str = UnitSystem.SI.value,
    url_params: dict = None,
):
    inputs = []
    all_inputs = set()

    for model in Models:
        for input_info in model.value.inputs:
            all_inputs.add(input_info.id)

    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    values: ModelInputsInfo
    for values in model_inputs:
        # print(f"input_values: {values}")
        if (
            values.id == ElementsIDs.met_input.value
            or values.id == ElementsIDs.clo_input.value
        ):
            inputs.append(create_autocomplete(values, url_params))
        else:
            # if the value is not in the URL params, use the default value
            default_value = (
                url_params.get(values.id, values.value) if url_params else values.value
            )

            input_filed = dmc.NumberInput(
                label=values.name + " (" + values.unit + ")",
                description=f"From {values.min} to {values.max}",
                value=default_value,
                min=values.min,
                max=values.max,
                step=values.step,
                id=values.id,
            )
            inputs.append(input_filed)

    unit_toggle = dmc.Center(
        dmc.Switch(
            id=ElementsIDs.UNIT_TOGGLE.value,
            label=f"{units} Units",
            checked=units == UnitSystem.IP.value,
        )
    )

    inputs.append(unit_toggle)
    # show custom ensemble button
    custom_ensemble_button = None
    if selected_model in [Models.PMV_EN.name, Models.PMV_ashrae.name]:
        custom_ensemble_button = dmc.Button(
            "Custom Ensemble",
            id=ElementsIDs.modal_custom_ensemble_open.value,
        )

    return dmc.Paper(
        children=[
            dmc.Stack(
                [
                    html.Form(
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    dmc.Stack(inputs, gap="xs"), span={"base": 12}
                                ),
                            ],
                            gutter="md",
                        ),
                        id=ElementsIDs.inputs_form.value,
                    ),
                    custom_ensemble_button,
                    modal_custom_ensemble() if custom_ensemble_button else None,
                ],
                gap="xs",
            ),
        ],
        shadow="md",
        p="md",
    )


# Custom Ensemble
@callback(
    Output(ElementsIDs.modal_custom_ensemble.value, "opened"),
    Output(ElementsIDs.clo_input.value, "value", allow_duplicate=True),
    Output(ElementsIDs.modal_custom_ensemble_warning.value, "display"),
    Output(ElementsIDs.modal_custom_ensemble_warning.value, "children"),
    Input(ElementsIDs.modal_custom_ensemble_value.value, "value"),
    Input(ElementsIDs.modal_custom_ensemble_open.value, "n_clicks"),
    Input(ElementsIDs.modal_custom_ensemble_close.value, "n_clicks"),
    Input(ElementsIDs.modal_custom_ensemble_submit.value, "n_clicks"),
    State(ElementsIDs.modal_custom_ensemble.value, "opened"),
    State(ElementsIDs.MODEL_SELECTION.value, "value"),
    prevent_initial_call=True,
)
def handle_modal(clo_value, _nc_open, _nc_close, _nc_submit, opened, selected_model):

    ctx = dash.callback_context.triggered_id

    if ctx == ElementsIDs.modal_custom_ensemble_open.value:
        return True, dash.no_update, "none", dash.no_update

    if ctx == ElementsIDs.modal_custom_ensemble_close.value:
        return False, dash.no_update, "none", dash.no_update

    total_clo_value = 0
    for value in clo_value:
        total_clo_value += float(value.split("_")[0])
    total_clo_value = round(total_clo_value, 2)

    model_info = Models[selected_model].value
    max_clo_value = [
        input_info.max
        for input_info in model_info.inputs
        if input_info.id == ElementsIDs.clo_input.value
    ][0]

    min_clo_value = [
        input_info.min
        for input_info in model_info.inputs
        if input_info.id == ElementsIDs.clo_input.value
    ][0]

    if total_clo_value > max_clo_value:
        error_message = f"{TextWarning.clo_warning_exceed.value} {max_clo_value}{TextWarning.clo_warning_current_total.value} {total_clo_value} {TextWarning.clo_warning_clo.value}"
        return dash.no_update, dash.no_update, "block", error_message

    if total_clo_value < min_clo_value:
        error_message = f"{TextWarning.clo_warning_less.value} {min_clo_value}{TextWarning.clo_warning_current_total.value} {total_clo_value} {TextWarning.clo_warning_clo.value}"
        return dash.no_update, dash.no_update, "block", error_message

    if ctx == ElementsIDs.modal_custom_ensemble_submit.value:
        return False, total_clo_value, "none", dash.no_update

    return opened, dash.no_update, "none", dash.no_update


def create_autocomplete(values: ModelInputsInfo, url_params: dict):
    default_value = (
        url_params.get(values.id, values.value) if url_params else values.value
    )
    return dmc.Autocomplete(
        id=values.id,
        label=f"{values.name} ({values.unit})",
        placeholder=f"Enter a value or select a {values.name}",
        data=[],
        value=str(default_value),
        description=f"From {values.min} to {values.max}",
    )


def update_options(input_value, options, selection_enum):
    if input_value is None or input_value == "":
        return [], ""

    option_values = [option.value for option in selection_enum]

    if input_value in option_values:
        return option_values, float(input_value.split(":")[-1].strip().split()[0])

    try:
        input_number = float(input_value)
        filtered_options = []
        for option in selection_enum:
            # Extract the value
            option_value = float(option.value.split(":")[-1].strip().split()[0])
            # Perform comparison
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)

        if not filtered_options:
            return option_values, input_value
    except ValueError:
        filtered_options = [
            option for option in option_values if input_value.lower() in option.lower()
        ]
        if not filtered_options:
            return option_values, ""

    return filtered_options, input_value


@callback(
    Output(ElementsIDs.met_input.value, "data"),
    Output(ElementsIDs.met_input.value, "value"),
    Input(ElementsIDs.met_input.value, "value"),
    State(ElementsIDs.met_input.value, "data"),
)
def update_metabolic_rate_options(input_value, _):
    return update_options(input_value, MetabolicRateSelection, MetabolicRateSelection)


@callback(
    Output(ElementsIDs.clo_input.value, "data"),
    Output(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.clo_input.value, "value"),
    State(ElementsIDs.clo_input.value, "data"),
)
def update_clothing_level_options(input_value, _):
    return update_options(input_value, ClothingSelection, ClothingSelection)
