from aws_cdk import Stack
from aws_cdk.aws_apigatewayv2 import CfnApi
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from b_cfn_custom_userpool_authorizer.config.user_pool_ssm_config import UserPoolSsmConfig

from b_cfn_api_v2.api import Api
from b_cfn_api_v2_test.integration.infrastructure.user_pool_stack import UserPoolStack


class ApiStack(Stack):
    def __init__(self, scope: Stack, user_pool_stack: UserPoolStack):
        super().__init__(
            scope=scope,
            id='ApiStack'
        )

        prefix = TestingStack.global_prefix()

        self.api = Api(
            scope=self,
            id='Api',
            name=f'{prefix}Api',
            description='Sample description.',
            protocol_type='HTTP',
            cors_configuration=CfnApi.CorsProperty(
                allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
                allow_origins=['*'],
                allow_headers=[
                    'Content-Type',
                    'Authorization'
                ],
                max_age=300
            )
        )

        self.api.enable_api_key_authorizer()
        self.api.enable_authorizer(UserPoolSsmConfig(
            user_pool_id_ssm_key=user_pool_stack.ssm_pool_id.parameter_name,
            user_pool_client_id_ssm_key=user_pool_stack.ssm_pool_client_id.parameter_name,
            user_pool_region_ssm_key=user_pool_stack.ssm_pool_region.parameter_name,
        ), cache_ttl=0)

        self.api.enable_default_stage('test', enable_logging=True)
