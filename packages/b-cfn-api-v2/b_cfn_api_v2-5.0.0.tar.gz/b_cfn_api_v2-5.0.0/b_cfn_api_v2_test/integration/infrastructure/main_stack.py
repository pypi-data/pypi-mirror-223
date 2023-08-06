from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from constructs import Construct

from b_cfn_api_v2_test.integration.infrastructure.api_stack import ApiStack
from b_cfn_api_v2_test.integration.infrastructure.authorized_endpoint_api_key_stack import AuthorizedEndpointApiKeyStack
from b_cfn_api_v2_test.integration.infrastructure.authorized_endpoint_user_pool_stack import \
    AuthorizedEndpointUserPoolStack
from b_cfn_api_v2_test.integration.infrastructure.user_pool_stack import UserPoolStack


class MainStack(TestingStack):
    USER_POOL_ENDPOINT_KEY = 'UserPoolEndpoint'
    API_KEY_ENDPOINT_KEY = 'ApiKeyEndpoint'
    USER_POOL_ID_KEY = 'UserPoolId'
    USER_POOL_CLIENT_ID_KEY = 'UserPoolClientId'
    API_KEYS_GENERATOR_FUNCTION_KEY = 'ApiKeysGeneratorFunction'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope)

        self.user_pool_stack = UserPoolStack(self)
        self.api_stack = ApiStack(self, self.user_pool_stack)
        AuthorizedEndpointApiKeyStack(self, self.api_stack.api)
        AuthorizedEndpointUserPoolStack(self, self.api_stack.api)

        self.add_output(self.USER_POOL_ENDPOINT_KEY, value=f'{self.api_stack.api.full_url}/dummy1')
        self.add_output(self.API_KEY_ENDPOINT_KEY, value=f'{self.api_stack.api.full_url}/dummy2')
        self.add_output(self.USER_POOL_ID_KEY, value=self.user_pool_stack.pool.user_pool_id)
        self.add_output(self.USER_POOL_CLIENT_ID_KEY, value=self.user_pool_stack.client.user_pool_client_id)
        self.add_output(self.API_KEYS_GENERATOR_FUNCTION_KEY, value=self.api_stack.api.api_key_authorizer.generator_function.function_name)
