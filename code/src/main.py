import asyncio
import os

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
    return {"Hello": "World"}


handler = Mangum(app)

if "AWS_EXECUTION_ENV" in os.environ:
    print("Running in AWS mode")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.router.startup())
