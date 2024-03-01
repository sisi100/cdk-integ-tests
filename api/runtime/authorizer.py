import os

import boto3

table_name = os.getenv("TABLE_NAME")
table = boto3.resource("dynamodb").Table(table_name)


def handler(event, context):
    token = event["authorizationToken"]
    resources = [event["methodArn"]]
    return authorizer(token, resources)


def authorizer(user_id, resources):
    """
    認証処理（実運用でこんな認証しないでね）

    テーブルにidがあれば成功。なければ失敗。
    """
    context = {}
    effect = "Deny"
    try:
        response = table.get_item(Key={"pk": user_id})
        context["userName"] = response["Item"]["user_name"]
        effect = "Allow"
    except Exception as e:
        # 認証失敗
        pass
    return {
        "principalId": "hoge",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{"Action": "execute-api:Invoke", "Effect": effect, "Resource": resources}],
        },
        "context": context,
    }
