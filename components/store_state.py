import re
from urllib.parse import urlparse, parse_qs
from dash import no_update, ctx, dcc
from dash.dependencies import Input, Output, State, ALL


def setup_dash_callbacks(app, store_id):
    """Set up Dash callbacks to manage dcc.Store data, supporting multiple dynamic input components."""

    @app.callback(
        Output(store_id, "data"),
        [Input({"type": "dynamic-input", "index": ALL}, "value"),
         Input('url', 'href')],
        State(store_id, "data"),
        prevent_initial_call=True,
    )
    def manage_store_data(input_values, url, store_data):
        if store_data is None or not isinstance(store_data, dict):
            store_data = {}

        # Update store data with dynamic input values
        if ctx.triggered:
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Save dynamic input values
            if 'dynamic-input' in triggered_id:
                prop_id = ctx.triggered[0]['prop_id']
                value = ctx.triggered[0]['value']
                # Use regex to find the index after "index":
                match = re.search(r'"index":"?([^"]+)"?', prop_id)
                if match:
                    index = match.group(1).replace(',', '')
                    store_data = StoreState.save_state_to_store(store_data, index, value)

            # Save URL
            if 'url' in triggered_id:
                parsed_url = StoreState.parse_url(url)

                path = parsed_url['path']
                query_params = parsed_url['query_params']
                path_parts = parsed_url['path_parts']

                # Extract model and type based on URL path
                if len(path_parts) == 2:
                    model = path_parts[0]
                    type_part = path_parts[1]
                    store_data = StoreState.save_state_to_store(store_data, 'model', model)
                    store_data = StoreState.save_state_to_store(store_data, 'type', type_part)
                elif len(path_parts) == 1:
                    model = path_parts[0]
                    store_data = StoreState.save_state_to_store(store_data, 'model', model)
                    store_data = StoreState.save_state_to_store(store_data, 'type', '')
                for key, value in query_params.items():
                    value = value[0]
                    store_data = StoreState.save_state_to_store(store_data, key, value)

        return store_data

    @app.callback(
        Output({"type": "dynamic-input", "index": ALL}, "value"),
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
                        if output['id']['index'] == key:
                            input_values[i] = value

            return input_values

        # If modified_timestamp is empty or invalid, return a list with no_update
        return [no_update] * len(ctx.outputs_list)


class StoreState:
    def __init__(self, store_type="session"):
        """Initialize StoreState class and set the storage type for dcc.Store."""
        self.store_type = store_type  # Set storage type

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
        path_parts = parsed_url.path.strip('/').split('/')

        return {
            'path': parsed_url.path,
            'query_params': query_params,
            'fragment': parsed_url.fragment,
            'path_parts': path_parts
        }
