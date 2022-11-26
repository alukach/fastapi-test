import os

import boto3
from fastapi import FastAPI
from mangum import Mangum



app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("starting app")


@app.on_event("shutdown")
async def shutdown_event():
    print("shutting down app")


@app.get("/")
def read_root():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=os.environ["secret_arn"])
    return response["SecretString"]

@app.get("/secret")
def read_root():
    return os.environ['secret_value']


handler = Mangum(app)
