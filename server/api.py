from server.routes import router as TodoRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://front-end-bagzcode.vercel.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to my todo application, use the /docs route to proceed"
    }

app.include_router(TodoRouter)
