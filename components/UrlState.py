import json
from urllib.parse import urlparse, parse_qs, urlencode

from dash import ctx, dash
from dash.dependencies import Input, Output, State, ALL


class UrlState:
    @staticmethod
    def encode_state(state_dict):
        """Encode a state dictionary into a URL query string."""
        encoded_state = {}
        for key, value in state_dict.items():
            if isinstance(value, (dict, list)):
                encoded_state[key] = json.dumps(value)
            else:
                encoded_state[key] = value
        return "?" + urlencode(encoded_state)

    @staticmethod
    def parse_state(url):
        """Parse a URL and extract the state dictionary."""
        parse_result = urlparse(url)
        state_dict = parse_qs(parse_result.query)

        for key, value in state_dict.items():
            if isinstance(value, list) and len(value) == 1:
                try:
                    state_dict[key] = json.loads(value[0])
                except json.JSONDecodeError:
                    state_dict[key] = value[0]

        return state_dict

    @staticmethod
    def add_single_page_state(model, params):
        """Generate URL state for single page."""
        state = {"model": model, **params}
        return UrlState.encode_state(state)

    @staticmethod
    def add_compare_inputs_state(model, set1, set2):
        """Generate URL state for compare inputs page."""
        state = {
            "model": model,
            "set1": ",".join([f"{k}={v}" for k, v in set1.items()]),
            "set2": ",".join([f"{k}={v}" for k, v in set2.items()]),
        }
        return UrlState.encode_state(state)

    @staticmethod
    def add_compare_models_state(models, params):
        """Generate URL state for compare models page."""
        state = {"models": ",".join(models), **params}
        return UrlState.encode_state(state)

    @staticmethod
    def add_range_state(model, range_params):
        """Generate URL state for range page."""
        state = {"model": model}
        for key, value in range_params.items():
            state[key] = f"{value[0]}-{value[1]}"
        return UrlState.encode_state(state)

    @staticmethod
    def parse_set_params(param_string):
        """Parse set parameters from a string."""
        return dict(item.split("=") for item in param_string.split(",") if item)

    @staticmethod
    def setup_dash_callbacks(app):
        # todo why the callback is defined inside the function?
        """Set up Dash callbacks for URL state management."""

        @app.callback(
            Output("url", "search"),
            [
                Input({"type": "model-dropdown", "page": ALL}, "value"),
                Input({"type": "single-input", "index": ALL}, "value"),
                Input({"type": "compare-input-1", "index": ALL}, "value"),
                Input({"type": "compare-input-2", "index": ALL}, "value"),
                Input({"type": "compare-models-input", "index": ALL}, "value"),
                Input({"type": "range-input", "index": ALL}, "value"),
            ],
            [
                State({"type": "single-input", "index": ALL}, "id"),
                State({"type": "compare-input-1", "index": ALL}, "id"),
                State({"type": "compare-input-2", "index": ALL}, "id"),
                State({"type": "compare-models-input", "index": ALL}, "id"),
                State({"type": "range-input", "index": ALL}, "id"),
                State("url", "pathname"),
            ],
        )
        def update_url(*args):
            if not ctx.triggered:
                return dash.no_update

            # todo trigger_id is initialised but not used
            triggered_id = ctx.triggered[0]["prop_id"]
            pathname = args[-1]

            # todo path should be taken from a global class
            if pathname == "/single":
                model = args[0][0]
                inputs = args[1]
                input_ids = args[6]
                params = {
                    id["index"]: value
                    for id, value in zip(input_ids, inputs)
                    if value is not None
                }
                return UrlState.add_single_page_state(model, params)

            elif pathname == "/compare/inputs":
                model = args[0][0]
                set1_inputs = args[2]
                set2_inputs = args[3]
                set1_ids = args[7]
                set2_ids = args[8]
                set1 = {
                    id["index"]: value
                    for id, value in zip(set1_ids, set1_inputs)
                    if value is not None
                }
                set2 = {
                    id["index"]: value
                    for id, value in zip(set2_ids, set2_inputs)
                    if value is not None
                }
                return UrlState.add_compare_inputs_state(model, set1, set2)

            elif pathname == "/compare/models":
                selected_models = args[0][0]
                inputs = args[4]
                input_ids = args[9]
                params = {
                    id["index"]: value
                    for id, value in zip(input_ids, inputs)
                    if value is not None
                }
                return UrlState.add_compare_models_state(selected_models, params)

            elif pathname == "/range":
                model = args[0][0]
                range_inputs = args[5]
                range_ids = args[10]
                range_params = {
                    id["index"]: value
                    for id, value in zip(range_ids, range_inputs)
                    if value is not None
                }
                return UrlState.add_range_state(model, range_params)

            return dash.no_update

    @staticmethod
    def get_current_values_from_dash(values, ids):
        """Extract current values from Dash callback context."""
        return {
            id_dict["index"]: value
            for id_dict, value in zip(ids, values)
            if value is not None
        }

    @staticmethod
    def generate_url(page, **kwargs):
        """Generate a URL for a specific page with given parameters."""
        # todo page should be taken from a global class
        if page == "single":
            return f"/single{UrlState.add_single_page_state(kwargs['model'], kwargs['params'])}"
        elif page == "compare_inputs":
            return f"/compare/inputs{UrlState.add_compare_inputs_state(kwargs['model'], kwargs['set1'], kwargs['set2'])}"
        elif page == "compare_models":
            return f"/compare/models{UrlState.add_compare_models_state(kwargs['models'], kwargs['params'])}"
        elif page == "range":
            return f"/range{UrlState.add_range_state(kwargs['model'], kwargs['range_params'])}"
        else:
            raise ValueError(f"Unknown page: {page}")
