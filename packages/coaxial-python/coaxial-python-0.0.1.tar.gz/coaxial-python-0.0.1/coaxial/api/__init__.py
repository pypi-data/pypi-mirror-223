# flake8: noqa

# import apis into api package
from coaxial.api.auth_integration_api import AuthIntegrationApi
from coaxial.api.data_integration_api import DataIntegrationApi
from coaxial.api.function_api import FunctionApi
from coaxial.api.model_integration_api import ModelIntegrationApi
from coaxial.api.provision_api import ProvisionApi


# import api client
from coaxial.api_client import ApiClient
from coaxial.configuration import Configuration, Environment

class Api(object):

    def __init__(
        self,
        host=None,
        environment: Environment = None,
        api_key=None,
        api_key_prefix=None,
        username=None,
        password=None,
        discard_unknown_keys=False,
        disabled_client_side_validations="",
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
        ssl_ca_cert=None,
    ):
        configuration = Configuration(
            host,
            environment,
            api_key,
            api_key_prefix,
            username,
            password,
            discard_unknown_keys,
            disabled_client_side_validations,
            server_index,
            server_variables,
            server_operation_index,
            server_operation_variables,
            ssl_ca_cert,
        )
        api_client = ApiClient(configuration)
        self.auth_integration = AuthIntegrationApi(api_client)
        self.data_integration = DataIntegrationApi(api_client)
        self.function = FunctionApi(api_client)
        self.model_integration = ModelIntegrationApi(api_client)
        self.provision = ProvisionApi(api_client)
        


