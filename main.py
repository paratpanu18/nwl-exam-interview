from fastapi import FastAPI
from fastapi_pagination import add_pagination
import uvicorn

from src.settings import settings
from src.routers.api_router import api_router

app = FastAPI()
app.include_router(api_router)

add_pagination(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
