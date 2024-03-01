def handler(event, context):
    authorizer_context = event["requestContext"]["authorizer"]
    user_name = authorizer_context["userName"]
    return hello(user_name)


def hello(user_name):
    return {
        "statusCode": 200,
        "body": f"Hello {user_name} !",
    }
