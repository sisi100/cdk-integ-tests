import aws_cdk as cdk

from api.stack import Api

app = cdk.App()
api = Api(app, "cdk-integ-tests-stack")

app.synth()
