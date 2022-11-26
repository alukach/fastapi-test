#!/usr/bin/env python3
import os
from aws_cdk import App, Stack, CfnOutput
from aws_cdk.aws_lambda import Runtime, FunctionUrlAuthType
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_secretsmanager import Secret


class Stack(Stack):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        secret_name = os.environ["SECRET"]

        print(f'{secret_name=}')

        secret = Secret.from_secret_name_v2(
            self,
            "secret",
            secret_name=secret_name,
        )

        handler = PythonFunction(
            self,
            "MyFunction",
            entry="code",
            runtime=Runtime.PYTHON_3_8,
            index="src/main.py",
            handler="handler",
            environment={
                "secret_arn": secret.secret_arn,
                # I recommend against this
                "secret_value": secret.secret_value.unsafe_unwrap(),
            },
        )

        secret.grant_read(handler)

        function_url = handler.add_function_url(
            auth_type=FunctionUrlAuthType.NONE
        )

        CfnOutput(
            self,
            "api-url",
            value=function_url.url,
            export_name="url",
        )


app = App()


Stack(app, "Cross-Region-Secret-Access-Test")

app.synth()
