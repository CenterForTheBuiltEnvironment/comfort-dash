import dash
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, State
from components.drop_down_inline import generate_dropdown_selection

from components.dropdowns import options
from utils.my_config_file import (
    ModelInputsInfo,
    Models,
    convert_units,
    ElementsIDs,
    UnitSystem,
    MetabolicRateSelection,
    ClothingSelection,
    Functionalities,
    AdaptiveENSpeeds,
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
    function_selection: str = Functionalities.Default.value,
):
    inputs = []
    all_inputs = set()

    for model in Models:
        for input_info in model.value.inputs:
            all_inputs.add(input_info.id)
        if (
            selected_model in [Models.PMV_ashrae.name]
            and function_selection == Functionalities.Default.value
        ):
            for input_info in Models.PMV_ashrae.value.inputs2:
                all_inputs.add(input_info.id)

    model_inputs = Models[selected_model].value.inputs
    model_inputs = convert_units(model_inputs, units)

    def shared_label_and_description(values):
        return dmc.Stack(
            [
                dmc.Text(f"{values.name} ({values.unit})", size="sm"),
                dmc.Text(f"From {values.min} to {values.max}", size="xs", c="gray"),
            ],
            gap=0,
        )

    model_inputs2 = (
        convert_units(Models[selected_model].value.inputs2, units)
        if function_selection == Functionalities.Compare.value
        and selected_model in [Models.PMV_ashrae.name]
        else None
    )

    for idx, values in enumerate(model_inputs):
        input_id = values.id
        if input_id in all_inputs:
            default_input = None
            input_stack = None
            if input_id in {ElementsIDs.met_input.value, ElementsIDs.clo_input.value}:
                default_input = create_autocomplete(values)
            elif (
                selected_model == Models.Adaptive_EN.name
                or selected_model == Models.Adaptive_ASHRAE.name
            ) and input_id == ElementsIDs.v_input.value:
                default_input = create_select_component(values)
            else:
                default_input = dmc.NumberInput(
                    value=values.value,
                    min=values.min,
                    max=values.max,
                    step=values.step,
                    id=values.id,
                    debounce=True,
                )

            if function_selection == Functionalities.Compare.value and model_inputs2:
                comparison_values = model_inputs2[idx]

                if comparison_values.id in {
                    ElementsIDs.met_input_input2.value,
                    ElementsIDs.clo_input_input2.value,
                }:
                    comparision_input = create_autocomplete(comparison_values)
                    input_stack = dmc.Stack(
                        [
                            shared_label_and_description(values),
                            dmc.Grid(
                                children=[
                                    dmc.GridCol(default_input, span={"base": 6}),
                                    dmc.GridCol(comparision_input, span={"base": 6}),
                                ],
                                gutter="xs",
                            ),
                        ],
                        gap=0,
                    )
                else:
                    right_input = dmc.NumberInput(
                        value=comparison_values.value,
                        min=comparison_values.min,
                        max=comparison_values.max,
                        step=comparison_values.step,
                        id=comparison_values.id,
                    )
                    input_stack = dmc.Stack(
                        [
                            shared_label_and_description(values),
                            dmc.Grid(
                                children=[
                                    dmc.GridCol(default_input, span={"base": 6}),
                                    dmc.GridCol(right_input, span={"base": 6}),
                                ],
                                gutter="xs",
                            ),
                        ],
                        gap=0,
                    )
            else:
                input_stack = dmc.Stack(
                    [
                        shared_label_and_description(values),
                        default_input,
                    ],
                    gap=0,
                )
            inputs.append(input_stack)

    for input_id in all_inputs:
        if input_id not in [input_info.id for input_info in model_inputs]:
            inputs.append(html.Div(style={"display": "none"}, id=input_id))

    unit_toggle = dmc.Center(
        dmc.Switch(
            id=ElementsIDs.UNIT_TOGGLE.value,
            label=f"{units} Units",
            checked=units == UnitSystem.IP.value,
        )
    )
    inputs.append(unit_toggle)

    custom_ensemble_button = None
    if (
        selected_model in [Models.PMV_EN.name, Models.PMV_ashrae.name]
        and function_selection == Functionalities.Default.value
    ):
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
                                    dmc.Text("Inputs", fw=700),
                                ),
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


def create_autocomplete(values: ModelInputsInfo):
    return dmc.Autocomplete(
        id=values.id,
        # label=f"{values.name} ({values.unit})",
        placeholder=f"Enter a value or select a {values.name}",
        data=[],
        value=str(values.value),
        # description=f"From {values.min} to {values.max}",
    )


def create_select_component(values: ModelInputsInfo):
    air_speed_box = {
        "id": ElementsIDs.v_input.value,
        "question": None,
        "options": [speed.value for speed in AdaptiveENSpeeds],
        "multi": False,
        "default": values.value,
    }
    return generate_dropdown_selection(
        air_speed_box, clearable=False, only_dropdown=True
    )


def update_options(input_value, selection_enum, min_value, max_value):
    if input_value is None or input_value == "":
        return [], ""

    option_values = [option.value for option in selection_enum]

    if input_value in option_values:
        return option_values, float(input_value.split(":")[-1].strip().split()[0])

    try:
        input_number = float(input_value)
        if input_number < min_value:
            return option_values, min_value
        elif input_number > max_value:
            return option_values, max_value

        # input_number = float(input_value)
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
    return update_options(input_value, MetabolicRateSelection, 1.0, 4.0)


@callback(
    Output(ElementsIDs.clo_input.value, "data"),
    Output(ElementsIDs.clo_input.value, "value"),
    Input(ElementsIDs.clo_input.value, "value"),
    State(ElementsIDs.clo_input.value, "data"),
)
def update_clothing_level_options(input_value, _):
    return update_options(input_value, ClothingSelection, 0.0, 1.5)


@callback(
    Output(ElementsIDs.met_input_input2.value, "data"),
    Output(ElementsIDs.met_input_input2.value, "value"),
    Input(ElementsIDs.met_input_input2.value, "value"),
    State(ElementsIDs.met_input_input2.value, "data"),
)
def update_metabolic_rate_options(input_value, _):
    return update_options(input_value, MetabolicRateSelection, 1.0, 4.0)


@callback(
    Output(ElementsIDs.clo_input_input2.value, "data"),
    Output(ElementsIDs.clo_input_input2.value, "value"),
    Input(ElementsIDs.clo_input_input2.value, "value"),
    State(ElementsIDs.clo_input_input2.value, "data"),
)
def update_clothing_level_options(input_value, _):
    return update_options(input_value, ClothingSelection, 0.0, 1.5)


@callback(
    Output(ElementsIDs.v_input.value, "data"),
    Output(ElementsIDs.v_input.value, "value"),
    Input(ElementsIDs.v_input.value, "value"),
    State(ElementsIDs.v_input.value, "data"),
)
def update_adaptive_en_air_speed_options(input_value, _):
    return [speed.value for speed in AdaptiveENSpeeds], input_value
