from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes.data_routes import router as data_router
from backend.database import init_db


app = FastAPI(title="Trust Engine API")

@app.on_event("startup")
def startup_event():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router, prefix="/data")

app.mount(
    "/frontend",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)
