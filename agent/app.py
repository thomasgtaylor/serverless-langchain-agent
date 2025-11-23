import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .dependencies import get_openai_api_key
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_openai_api_key()
    yield


app = FastAPI(
    title="Serverless LangChain Agent",
    description="A serverless LangChain agent built with AWS CDK, Lambda, and FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
