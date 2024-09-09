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
                                    {"value": "0.01_Bra", "label": "Bra"},
                                    {"value": "0.03", "label": "Women's underwear"},
                                    {"value": "0.04", "label": "Men's underwear"},
                                    {"value": "0.14_Half_slip", "label": "Half slip"},
                                    {
                                        "value": "0.15_Long_underwear_bottoms",
                                        "label": "Long underwear bottoms",
                                    },
                                    {"value": "0.16", "label": "Full slip"},
                                    {
                                        "value": "0.20_Long_underwear",
                                        "label": "Long underwear top",
                                    },
                                ],
                            },
                            {
                                "group": "Tops",
                                "items": [
                                    # todo change these values
                                    {"value": "0.08_T_shirt", "label": "T-shirt"},
                                    {
                                        "value": "0.12",
                                        "label": "Sleeveless scoop-neck blouse",
                                    },
                                    {
                                        "value": "0.17",
                                        "label": "Short-sleeve knit shirt",
                                    },
                                    {
                                        "value": "0.10_Sleevelss_vest_thin",
                                        "label": "Sleeveless vest (thin)",
                                    },
                                    {
                                        "value": "0.17_Sleevelss_vest_thick",
                                        "label": "Sleeveless vest (thick)",
                                    },
                                    {
                                        "value": "0.18",
                                        "label": "Sleeveless short gown (thin)",
                                    },
                                    {
                                        "value": "0.19",
                                        "label": "Short-sleeve dress shirt",
                                    },
                                    {
                                        "value": "0.20_Sleevelss_long_gown_thin",
                                        "label": "Sleeveless long gown (thin)",
                                    },
                                    {
                                        "value": "0.25_Long_sleeve_dress_shirt",
                                        "label": "Long-sleeve dress shirt",
                                    },
                                    {
                                        "value": "0.34",
                                        "label": "Long-sleeve flannel shirt",
                                    },
                                    {
                                        "value": "0.34_Long_sleeve_sweat_shirt",
                                        "label": "Long-sleeve sweat shirt",
                                    },
                                    {
                                        "value": "0.31",
                                        "label": "Short-sleeve hospital gown",
                                    },
                                    {
                                        "value": "0.34_Short_sleeve_short_robe_thin",
                                        "label": "Short-sleeve short robe (thin)",
                                    },
                                    {
                                        "value": "0.42_Short_sleeve_pajamas",
                                        "label": "Short-sleeve pajamas",
                                    },
                                    {
                                        "value": "0.46",
                                        "label": "Short-sleeve long gown",
                                    },
                                    {
                                        "value": "0.48",
                                        "label": "Short-sleeve short wrap robe (thick)",
                                    },
                                    {
                                        "value": "0.57",
                                        "label": "Short-sleeve pajamas (thick)",
                                    },
                                    {
                                        "value": "0.69",
                                        "label": "Short-sleeve long wrap robe (thick)",
                                    },
                                    {"value": "0.30", "label": "Overalls"},
                                    {"value": "0.49", "label": "Coveralls"},
                                    {
                                        "value": "0.23",
                                        "label": "Sleeveless, scoop-neck shirt (thin)",
                                    },
                                    {
                                        "value": "0.27",
                                        "label": "Sleeveless, scoop-neck shirt (thick)",
                                    },
                                    {
                                        "value": "0.13",
                                        "label": "Sleeveless vest (thin)",
                                    },
                                    {
                                        "value": "0.22",
                                        "label": "Sleeveless vest (thick)",
                                    },
                                    {
                                        "value": "0.25",
                                        "label": "Long sleeve shirt (thin)",
                                    },
                                    {
                                        "value": "0.36_Long_sleeve_shirt_thick",
                                        "label": "Long sleeve shirt (thick)",
                                    },
                                    {
                                        "value": "0.36",
                                        "label": "Single-breasted coat (thin)",
                                    },
                                    {
                                        "value": "0.44",
                                        "label": "Single-breasted coat (thick)",
                                    },
                                    {
                                        "value": "0.42",
                                        "label": "Double-breasted coat (thin)",
                                    },
                                    {
                                        "value": "0.48_Double_breasted_coat_thick",
                                        "label": "Double-breasted coat (thick)",
                                    },
                                ],
                            },
                            {
                                "group": "Trousers",
                                "items": [
                                    {
                                        "value": "0.06_Short_shorts",
                                        "label": "Short shorts",
                                    },
                                    {"value": "0.08", "label": "Walking shorts"},
                                    {"value": "0.14", "label": "Thin skirt"},
                                    {
                                        "value": "0.23_Thick_skirt",
                                        "label": "Thick skirt",
                                    },
                                    {
                                        "value": "0.15_Thin_trousers",
                                        "label": "Thin trousers",
                                    },
                                    {"value": "0.24", "label": "Thick trousers"},
                                    {"value": "0.28", "label": "Sweatpants"},
                                    {
                                        "value": "0.33",
                                        "label": "Long-sleeve shirtdress (thin)",
                                    },
                                    {
                                        "value": "0.47",
                                        "label": "Long-sleeve shirtdress (thick)",
                                    },
                                    {
                                        "value": "0.29",
                                        "label": "Short-sleeve shirtdress",
                                    },
                                ],
                            },
                            {
                                "group": "Socks",
                                "items": [
                                    {
                                        "value": "0.02_Ankle_socks",
                                        "label": "Ankle socks",
                                    },
                                    {"value": "0.02_Panty_hose", "label": "Panty hose"},
                                    {
                                        "value": "0.03_Claf_length_socks",
                                        "label": "Calf length socks",
                                    },
                                    {"value": "0.06", "label": "Knee socks (thick)"},
                                ],
                            },
                            {
                                "group": "Shoes",
                                "items": [
                                    {"value": "0.02", "label": "Shoes or sandals"},
                                    {"value": "0.03_Slippers", "label": "Slippers"},
                                    {"value": "0.10_Boots", "label": "Boots"},
                                ],
                            },
                            {
                                "group": "Chair",
                                "items": [
                                    {"value": "0.00", "label": "Metal chair"},
                                    {"value": "0.01", "label": "Wooden stool"},
                                    {"value": "0.10", "label": "Standard office chair"},
                                    {"value": "0.15", "label": "Executive chair"},
                                ],
                            },
                        ],
                        styles={"dropdown": {"z-index": "10002"}},
                        # w=400,
                    ),
                    dmc.Group(
                        [
                            # todo when we press submit we should update the clo value in the inputs
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
    selected_model: str = "PMV_ashrae", units: str = UnitSystem.SI.value
):
    inputs = []
    # create empty collection to keep track of the input field names that have been added
    added_inputs = set()
    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    values: ModelInputsInfo
    for values in model_inputs:
        # Checks whether the current input field name already exists in the collection
        if values.name in added_inputs:
            continue  # if already exists, skip the loop to prevent repeated addition

        if values.name == "Metabolic Rate":
            metabolic_input = create_metabolic_rate_input(values)
            inputs.append(metabolic_input)
        elif values.name == "Clothing Level":
            clothing_input = create_clothing_level_input(values)
            inputs.append(clothing_input)
        else:
            input_filed = dmc.NumberInput(
                label=values.name + " (" + values.unit + ")",
                description=f"From {values.min} to {values.max}",
                value=values.value,
                min=values.min,
                max=values.max,
                step=values.step,
                id=values.id,
            )
            inputs.append(input_filed)

        added_inputs.add(values.name)

    unit_toggle = dmc.Center(
        dmc.Switch(
            id=ElementsIDs.UNIT_TOGGLE.value,
            label=f"{units} Units",
            checked=units == UnitSystem.IP.value,
        )
    )

    inputs.append(unit_toggle)

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
                    dmc.Button(
                        "Custom Ensemble",
                        id=ElementsIDs.modal_custom_ensemble_open.value,
                    ),
                    modal_custom_ensemble(),
                ],
                gap="xs",
            )
        ],
        shadow="md",
        p="md",
    )


# Custom Ensemble
@callback(
    Output(ElementsIDs.modal_custom_ensemble.value, "opened"),
    Output(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.modal_custom_ensemble_value.value, "value"),
    Input(ElementsIDs.modal_custom_ensemble_open.value, "n_clicks"),
    Input(ElementsIDs.modal_custom_ensemble_close.value, "n_clicks"),
    Input(ElementsIDs.modal_custom_ensemble_submit.value, "n_clicks"),
    State(ElementsIDs.modal_custom_ensemble.value, "opened"),
    prevent_initial_call=True,
)
def handle_modal(clo_value, _nc_open, _nc_close, _nc_submit, opened):

    ctx = dash.callback_context.triggered_id

    if ctx == ElementsIDs.modal_custom_ensemble_open.value:
        return True, dash.no_update

    if ctx == ElementsIDs.modal_custom_ensemble_close.value:
        return False, dash.no_update

    total_clo_value = 0
    for value in clo_value:
        total_clo_value += float(value.split("_")[0])
    total_clo_value = round(total_clo_value, 2)

    if ctx in [
        ElementsIDs.modal_custom_ensemble_submit.value,
    ]:
        return False, total_clo_value

    return opened, dash.no_update


def create_metabolic_rate_input(values: ModelInputsInfo):
    return dmc.Autocomplete(
        id=values.id,
        label=f"{values.name} ({values.unit})",
        placeholder="Enter a value or select an activity",
        data=[],
        value=str(values.value),
        description=f"From {values.min} to {values.max}",
    )


@callback(
    Output(ElementsIDs.met_input.value, "data"),
    Output(ElementsIDs.met_input.value, "value"),
    Input(ElementsIDs.met_input.value, "value"),
    State(ElementsIDs.met_input.value, "data"),
)
def update_metabolic_rate_options(input_value, current_data):
    if input_value is None or input_value == "":
        return [], ""

    try:
        input_number = float(input_value)
    except ValueError:
        return [option.value for option in MetabolicRateSelection], input_value

    # filter options based on input value
    filtered_options = []
    for option in MetabolicRateSelection:
        try:
            option_value = float(option.value.split(":")[-1].strip())
            # select the related options
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)
        except ValueError:
            # skip if the option doesn't have a numeric value
            continue

    # If no close matches, return all options
    if not filtered_options:
        filtered_options = [option.value for option in MetabolicRateSelection]

    return filtered_options, input_value


@callback(
    Output(ElementsIDs.met_input.value, "value", allow_duplicate=True),
    Input(ElementsIDs.met_input.value, "value"),
    prevent_initial_call=True,
)
def update_input_on_selection(selected_value):
    if selected_value in [option.value for option in MetabolicRateSelection]:
        try:
            return float(selected_value.split(":")[-1].strip().split()[0])
        except IndexError:
            return "0.8" if "Reclining" in selected_value else selected_value

    # print(float(selected_value.split(":")[-1].strip().split()[0]))
    return selected_value


# ---------------------clo
def create_clothing_level_input(values: ModelInputsInfo):
    return dmc.Autocomplete(
        id=values.id,
        label=f"{values.name} ({values.unit})",
        placeholder="Enter a value or select clothing",
        data=[],
        value=str(values.value),
        description=f"From {values.min} to {values.max}",
    )


@callback(
    Output(ElementsIDs.clo_input.value, "data"),
    Output(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.clo_input.value, "value"),
    State(ElementsIDs.clo_input.value, "data"),
)
def update_clothing_level_options(input_value, current_data):
    if input_value is None or input_value == "":
        return [], ""
    try:
        input_number = float(input_value)
    except ValueError:
        return [option.value for option in ClothingSelection], input_value

    filtered_options = []
    for option in ClothingSelection:
        try:
            option_value = float(option.value.split(":")[-1].strip().split()[0])
            if abs(option_value - input_number) < 1:
                filtered_options.append(option.value)
        except ValueError:
            continue

    if not filtered_options:
        filtered_options = [option.value for option in ClothingSelection]
    return filtered_options, input_value


@callback(
    Output(ElementsIDs.clo_input.value, "value", allow_duplicate=True),
    Input(ElementsIDs.clo_input.value, "value"),
    prevent_initial_call=True,
)
def update_clothing_input_on_selection(selected_value):
    if selected_value in [option.value for option in ClothingSelection]:
        try:
            return float(selected_value.split(":")[-1].strip().split()[0])
        except IndexError:
            return selected_value
    return selected_value

