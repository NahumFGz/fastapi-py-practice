from fastapi import FastAPI

app = FastAPI()


@app.get("/api-endpoint")
async def firt_api():
    return {"message": "Hello Nahum"}
