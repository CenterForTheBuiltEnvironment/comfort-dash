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
                for i, value in enumerate(input_values):
                    if value is not None:
                        key = f"input_{i}"
                        store_data = StoreState.save_state_to_store(
                            store_data, key, value
                        )
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

                # Initialize output list, default to using no_update
                input_values = [no_update] * num_outputs

                # Update existing data
                if store_data:
                    for i in range(num_outputs):
                        input_values[i] = store_data.get(f"input_{i}", no_update)

                return input_values

            # If modified_timestamp is empty or invalid, return a list of no_update
            return [no_update] * len(ctx.outputs_list)
