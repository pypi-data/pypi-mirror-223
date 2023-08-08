import uvicorn
from fastapi import FastAPI

from example.app.urls import app_router

app = FastAPI()

app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app)
