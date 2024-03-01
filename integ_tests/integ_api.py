import aws_cdk as cdk
from aws_cdk.cloud_assembly_schema import CdkCommands, DestroyCommand, DestroyOptions
from aws_cdk.integ_tests_alpha import ExpectedResult, IntegTest, Match
from cdk_integ_runner_cwd_fix import fix_cwd

fix_cwd()


from api.stack import Api

app = cdk.App()
api = Api(app, "cdk-integ-tests-stack-test")

integ = IntegTest(
    app,
    "integ",
    test_cases=[api],
    cdk_command_options=CdkCommands(destroy=DestroyCommand(args=DestroyOptions(force=True))),
)

# ------------------------------------
# 認証テスト
# ------------------------------------

# ==> 認証失敗（トークンなし）
integ.assertions.http_api_call(url=f"{api.url}/hello", method="GET", headers={}).expect(
    ExpectedResult.object_like(
        {
            "statusText": "Unauthorized",
            "status": 401,
        },
    )
)

# ==> 認証失敗（ユーザーなし）
integ.assertions.http_api_call(url=f"{api.url}/hello", method="GET", headers={"Authorization": "fuga"}).expect(
    ExpectedResult.object_like(
        {
            "statusText": "Forbidden",
            "status": 403,
        },
    )
)

# ==> 認証成功
integ.assertions.aws_api_call(
    # ユーザーを登録
    "DynamoDB",
    "putItem",
    {
        "TableName": api.table_name,
        "Item": {
            "pk": {"S": "hoge"},
            "user_name": {"S": "hoge太郎"},
        },
    },
).next(
    # リクエスト
    integ.assertions.http_api_call(url=f"{api.url}/hello", method="GET", headers={"Authorization": "hoge"}),
).expect(
    # 確認
    ExpectedResult.object_like(
        {
            "body": Match.string_like_regexp("hoge太郎"),
            "status": 200,
        },
    )
)

app.synth()
