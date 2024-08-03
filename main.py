from fastapi import FastAPI
from src.settings import settings
import uvicorn
from src.routers.criteria_type_router import criteria_type_router
from src.routers.interviewer_router import interviewer_router

from src.routers.interviewer_router import interviewer_router
from src.settings import settings

app = FastAPI()
app.include_router(interviewer_router)
app.include_router(criteria_type_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
