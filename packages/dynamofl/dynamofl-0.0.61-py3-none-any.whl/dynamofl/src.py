import logging

from .Helpers import Helpers
from .logging import set_logger
from .MessageHandler import _MessageHandler
from .State import _State

RETRY_AFTER = 5  # seconds


class DynamoFL:
    """Creates a client instance that communicates with the API through REST and websockets.
    ### Parameters
        token - Your auth token. Required.

        host - API server url. Defaults to DynamoFL prod API.

        metadata - Sets a default metadata object for attach_datasource calls; can be overriden.

        log_level - Set the log_level for the client. Accepts all of logging._Level. Defaults to logging.INFO.
    """

    def __init__(
        self,
        token: str,
        host: str = "https://api.dynamofl.com",
        metadata: object = None,
        log_level=logging.INFO,
    ):
        self._state = _State(token, host, metadata)

        self._messagehandler = _MessageHandler(self._state)
        self._messagehandler.connect_to_ws()

        set_logger(log_level=log_level)

    def attach_datasource(self, key, name=None, metadata=None):
        return self._state.attach_datasource(key, name, metadata)

    def delete_datasource(self, key):
        return self._state.delete_datasource(key)

    def get_datasources(self):
        return self._state.get_datasources()

    def delete_project(self, key):
        return self._state.delete_project(key)

    def get_user(self):
        return self._state.get_user()

    def create_project(self, base_model_path, params, dynamic_trainer_path=None):
        return self._state.create_project(base_model_path, params, dynamic_trainer_path)

    def get_project(self, project_key):
        return self._state.get_project(project_key)

    def get_projects(self):
        return self._state.get_projects()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        """
        Accepts a valid datasource_key and project_key
        Returns True if the datasource is labeled for the project; False otherwise

        """
        return self._state.is_datasource_labeled(
            project_key=project_key, datasource_key=datasource_key
        )

    def get_use_cases(self):
        self._state.get_use_cases()

    def get_datasets(self):
        self._state.get_datasets()

    def create_centralized_project(
        self, name=None, rounds=None, compute=None, use_case=None, dataset=None
    ):
        self._state.create_centralized_project(name, rounds, compute, use_case, dataset)

    def create_model(self, key: str, model_file_path, dataset_file_path, name: str, config):
        return self._state.create_model(key, model_file_path, dataset_file_path, name, config)

    def get_model(self, model_key: str):
        return self._state.get_model(model_key)

    def create_test(self, name: str, model_key: str, attack: str, config: list):
        return self._state.create_test(name, model_key, attack, config)