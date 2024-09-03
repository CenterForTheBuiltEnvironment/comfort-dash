import re

from dash import no_update, ctx, dcc
from dash.dependencies import Input, Output, State, ALL


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
        if store_data is None:
            store_data = {}
        store_data[key] = value
        return store_data

    @staticmethod
    def load_state_from_store(store_data, key):
        """Read data from dcc.Store."""
        if store_data and key in store_data:
            return store_data[key]
        return None

    def setup_dash_callbacks(self, app, store_id):
        """Set up Dash callbacks to manage dcc.Store data, supporting multiple dynamic input components."""

        @app.callback(
            Output(store_id, "data"),
            Input({"type": "dynamic-input", "index": ALL}, "value"),
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def save_data(input_values, store_data):
            # Update storage if triggered by input component
            if ctx.triggered:
                # Only get the first triggered item since ctx.triggered is usually a list of one
                prop_id = ctx.triggered[0]['prop_id']
                value = ctx.triggered[0]['value']

                # Use regex to find the index after "index":
                match = re.search(r'"index":"?([^"]+)"?', prop_id)

                if match:
                    index = match.group(1)
                    store_data = StoreState.save_state_to_store(store_data, index, value)

                return store_data
            return no_update

        @app.callback(
            Output({"type": "dynamic-input", "index": ALL}, "value"),
            Input(store_id, "modified_timestamp"),
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def load_data(modified_timestamp, store_data):
            if modified_timestamp:
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

