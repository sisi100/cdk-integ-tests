import pathlib

from aws_cdk import RemovalPolicy, Stack, aws_apigateway, aws_dynamodb, aws_lambda
from constructs import Construct


class Api(Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
    ):
        super().__init__(scope, id_)

        # DynamoDB
        table = aws_dynamodb.Table(
            self,
            "table",
            partition_key=aws_dynamodb.Attribute(name="pk", type=aws_dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Lambda
        code = aws_lambda.Code.from_asset(str(pathlib.Path(__file__).parent.joinpath("runtime").resolve()))

        authorizer_func = aws_lambda.Function(
            self,
            "authorizerFunc",
            code=code,
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="authorizer.handler",
            environment={"TABLE_NAME": table.table_name},
        )
        table.grant_read_data(authorizer_func)

        hello_func = aws_lambda.Function(
            self,
            "helloFunc",
            code=code,
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="hello.handler",
        )

        # API Gateway
        api = aws_apigateway.RestApi(self, "apiGateway")
        authorizer = aws_apigateway.TokenAuthorizer(
            self,
            "authorizer",
            identity_source=aws_apigateway.IdentitySource.header("Authorization"),
            handler=authorizer_func,
        )
        hello_resources = api.root.add_resource("hello")
        hello_resources.add_method("GET", aws_apigateway.LambdaIntegration(hello_func), authorizer=authorizer)

        # Output
        self.url = api.url
        self.table_name = table.table_name
