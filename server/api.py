from server.routes import router as TodoRouter
from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to my todo application, use the /docs route to proceed"
    }

app.include_router(TodoRouter)
