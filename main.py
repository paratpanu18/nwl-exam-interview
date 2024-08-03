from fastapi import FastAPI
from src.settings import Settings
import uvicorn
from src.routers.criteria_type_router import criteria_type_router

SETTINGS = Settings()

app = FastAPI()
app.include_router(criteria_type_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SETTINGS.PORT)