from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
)
from aws_cdk import (
    aws_dynamodb as dynamodb,
)
from aws_cdk import (
    aws_lambda as lambda_,
)
from aws_cdk import (
    aws_ssm as ssm,
)
from constructs import Construct


class ServerlessLangChainAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        openai_api_key = ssm.StringParameter.from_secure_string_parameter_attributes(
            self,
            "OpenAIApiKey",
            parameter_name="/langchain-agent/openai-api-key",
        )

        checkpoints_table = dynamodb.Table(
            self,
            "CheckpointsTable",
            table_name="checkpoints",
            partition_key=dynamodb.Attribute(
                name="PK", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            time_to_live_attribute="ttl",
        )

        func = lambda_.DockerImageFunction(
            self,
            "AgentFunction",
            code=lambda_.DockerImageCode.from_image_asset("./"),
            timeout=Duration.minutes(15),
            environment={
                "CHECKPOINTS_TABLE_NAME": checkpoints_table.table_name,
                "AWS_LWA_INVOKE_MODE": "RESPONSE_STREAM",
            },
        )

        openai_api_key.grant_read(func)
        checkpoints_table.grant_read_write_data(func)

        url = func.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            invoke_mode=lambda_.InvokeMode.RESPONSE_STREAM,
        )
        CfnOutput(
            self,
            "AgentFunctionUrl",
            value=url.url,
        )
