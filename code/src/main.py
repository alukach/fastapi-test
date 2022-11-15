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
