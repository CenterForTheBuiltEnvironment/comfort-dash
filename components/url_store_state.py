import re
from urllib.parse import urlparse, parse_qs
from dash import no_update, ctx, dcc
from dash.dependencies import Input, Output, State, ALL


class ParsedURL:
    def __init__(self, path, query_params, fragment, path_parts):
        self.path = path  # The path part of the URL
        self.query_params = query_params  # Query parameters in the URL
        self.fragment = fragment  # The fragment part of the URL
        self.path_parts = path_parts  # The different parts of the URL path


class StoreState:
    def __init__(self, persist_ids, store_type="session"):
        """
        Initialize StoreState class, set the storage type for dcc.Store, and set persistent IDs.

        :param persist_ids: List of IDs to be persisted
        :param store_type: Storage type, default is "session"
        """
        self.store_type = store_type  # Set storage type
        self.persist_ids = persist_ids  # Set persistent IDs

    def get_store_component(self, store_id):
        """
        Return the dcc.Store component using the specified storage type.

        :param store_id: ID for the store component
        :return: dcc.Store component
        """
        return dcc.Store(id=store_id, storage_type=self.store_type)

    @staticmethod
    def save_state_to_store(store_data, key, value):
        """
        Save data to dcc.Store.

        :param store_data: Current stored data
        :param key: Key of the data to be saved
        :param value: Value of the data to be saved
        :return: Updated store data
        """
        if store_data is None or not isinstance(store_data, dict):
            store_data = {}
        store_data[key] = value
        return store_data

    @staticmethod
    def load_state_from_store(store_data, key):
        """
        Read data from dcc.Store.

        :param store_data: Stored data
        :param key: Key of the data to be read
        :return: Value of the read data, or None if not found
        """
        if store_data and key in store_data:
            return store_data[key]
        return None

    @staticmethod
    def parse_url(url):
        """
        Parse the URL and extract useful information, returning a ParsedURL object.

        :param url: URL to be parsed
        :return: ParsedURL object containing parsed URL information
        """
        url = str(url)
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        path_parts = parsed_url.path.strip("/").split("/")

        # Return a ParsedURL object
        return ParsedURL(
            path=parsed_url.path,
            query_params=query_params,
            fragment=parsed_url.fragment,
            path_parts=path_parts
        )

    def update_local_storage(self, *args):
        """
        Update local storage.

        :param args: Input values and store data
        :return: Updated store data
        """
        *input_values, store_data = args
        if store_data is None:
            store_data = {}
        if ctx.triggered:
            triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
            value = ctx.triggered[0]["value"]
            store_data = self.save_state_to_store(store_data, triggered_id, value)
        return store_data

    def update_store_from_url(self, url, store_data):
        """
        Update store data based on URL.

        :param url: Current URL
        :param store_data: Current store data
        :return: Updated store data
        """
        if store_data is None:
            store_data = {}
        parsed_url = self.parse_url(url)

        # Update store data based on URL parameters
        for key, value in parsed_url.query_params.items():
            store_data = self.save_state_to_store(store_data, key, value[0])

        # Update model and type based on path
        if len(parsed_url.path_parts) >= 1:
            store_data = self.save_state_to_store(store_data, "model", parsed_url.path_parts[0])
        if len(parsed_url.path_parts) >= 2:
            store_data = self.save_state_to_store(store_data, "type", parsed_url.path_parts[1])

        return store_data

    def load_data(self, modified_timestamp, store_data):
        """
        Load data from storage.

        :param modified_timestamp: Modification timestamp
        :param store_data: Stored data
        :return: List of loaded data or list of no_update
        """
        if modified_timestamp and store_data:
            return [store_data.get(id, no_update) for id in self.persist_ids]
        return [no_update] * len(self.persist_ids)

    def update_url(self, *args):
        """
        Update URL based on store data.

        :param args: Input values, current URL, and store data
        :return: Updated URL or no_update
        """
        *values, current_url, store_data = args
        if store_data is None:
            return no_update

        # Construct new URL based on store_data
        parsed_url = urlparse(current_url)
        path = f"/{store_data.get('model', '')}"
        if 'type' in store_data:
            path += f"/{store_data['type']}"

        # Construct query parameter string
        query_params = "&".join([f"{id}={values[i]}" for i, id in enumerate(self.persist_ids) if values[i] is not None])

        # Create new URL
        new_url = parsed_url._replace(path=path, query=query_params).geturl()
        return new_url if new_url != current_url else no_update