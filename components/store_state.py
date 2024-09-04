import re
from urllib.parse import urlparse, parse_qs
from dash import no_update, ctx, dcc
from dash.dependencies import Input, Output, State, ALL

class StoreState:
    def __init__(self, persist_ids, store_type="session"):
        """Initialize StoreState class, set the storage type for dcc.Store, and set persistent IDs."""
        self.store_type = store_type  # Set storage type
        self.persist_ids = persist_ids  # Set persistent IDs

    def get_store_component(self, store_id):
        """Return the dcc.Store component using the specified storage type."""
        return dcc.Store(id=store_id, storage_type=self.store_type)

    @staticmethod
    def save_state_to_store(store_data, key, value):
        """Save data to dcc.Store."""
        if store_data is None or not isinstance(store_data, dict):
            store_data = {}
        store_data[key] = value
        return store_data

    @staticmethod
    def load_state_from_store(store_data, key):
        """Read data from dcc.Store."""
        if store_data and key in store_data:
            return store_data[key]
        return None

    @staticmethod
    def parse_url(url):
        """Parse URL and extract useful information."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        path_parts = parsed_url.path.strip("/").split("/")

        return {
            "path": parsed_url.path,
            "query_params": query_params,
            "fragment": parsed_url.fragment,
            "path_parts": path_parts
        }

    def setup_dash_callbacks(self, app, store_id):
        """Set up Dash callbacks to manage dcc.Store data, supporting multiple dynamic input components."""

        @app.callback(
            Output(store_id, "data"),
            [Input(id, "value") for id in self.persist_ids],
            [Input("url", "href")],
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def manage_store_data(*args):
            # The URL is the second-to-last argument
            url = args[-2]
            # store_data is the last argument
            store_data = args[-1]

            if store_data is None or not isinstance(store_data, dict):
                store_data = {}

            # Update store data with dynamic input values
            if ctx.triggered:
                triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

                # Save dynamic input values
                value = ctx.triggered[0]["value"]
                store_data = StoreState.save_state_to_store(store_data, triggered_id, value)

                # Save URL
                if "url" in triggered_id:
                    parsed_url = StoreState.parse_url(url)

                    path = parsed_url["path"]
                    query_params = parsed_url["query_params"]
                    path_parts = parsed_url["path_parts"]

                    # Extract model and type based on URL path
                    if len(path_parts) == 2:
                        model = path_parts[0]
                        type_part = path_parts[1]
                        store_data = StoreState.save_state_to_store(store_data, "model", model)
                        store_data = StoreState.save_state_to_store(store_data, "type", type_part)
                    elif len(path_parts) == 1:
                        model = path_parts[0]
                        store_data = StoreState.save_state_to_store(store_data, "model", model)
                        store_data = StoreState.save_state_to_store(store_data, "type", "")

                    for key, value in query_params.items():
                        value = value[0]
                        store_data = StoreState.save_state_to_store(store_data, key, value)

            return store_data

        @app.callback(
            [Output(id, "value") for id in self.persist_ids],
            Input(store_id, "modified_timestamp"),
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def load_data(modified_timestamp, store_data):
            if modified_timestamp:

                if store_data is None or not isinstance(store_data, dict):
                    store_data = {}

                # Get the current number of dynamic input components
                num_outputs = len(ctx.outputs_list)

                # Initialize the output list, defaulting to no_update
                input_values = [no_update] * num_outputs

                # If stored data exists, update the corresponding component values based on the indices
                if store_data:
                    # Iterate through the key-value pairs in the stored data
                    for key, value in store_data.items():
                        # Iterate through all the output components, matching the stored data indices
                        for i, output in enumerate(ctx.outputs_list):
                            # If the component's id matches the key in the stored data, update the component's value
                            if output["id"] == key:
                                input_values[i] = value

                return input_values

            # If modified_timestamp is empty or invalid, return a list with no_update
            return [no_update] * len(ctx.outputs_list)

        # 新增功能，反映到URL上
        @app.callback(
            Output("url", "search"),
            Input(store_id, "modified_timestamp"),
            State(store_id, "data"),
            prevent_initial_call=True,
        )

        def update_url(modified_timestamp, store_data):
            if modified_timestamp:
                url_tmp = store_data.get("url", None)
                model_tmp = store_data.get("model", None)
                type_tmp = store_data.get("type", None)

                url_tmp = re.match(r"^https?://[^/]+", url_tmp).group(0)

                if model_tmp == "single" or model_tmp == "range":
                    if not url_tmp.endswith("/"):
                        url_tmp += "/"
                    url_tmp += f"{model_tmp}?"
                else:
                    if not url_tmp.endswith("/"):
                        url_tmp += "/"
                    url_tmp += f"/{model_tmp}/{type_tmp}"

                for key, value in store_data.items():
                    if key not in ["model", "type", "url"]:
                        url_tmp += f"{key}={value}&"

                url_tmp = url_tmp[:-1]
                self.url = url_tmp

                return url_tmp

            return no_update
