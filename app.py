#!/usr/bin/env python3
from aws_cdk import core, aws_lambda_python, aws_lambda


class Stack(core.Stack):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        handler = aws_lambda_python.PythonFunction(
            self,
            "MyFunction",
            entry="code",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            index="src/main.py",
            handler="handler",
        )

        function_url = handler.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE
        )

        core.CfnOutput(
            self,
            "api-url",
            value=function_url.url,
            export_name="url",
        )


app = core.App()


Stack(app, "FastApiTest")

app.synth()
