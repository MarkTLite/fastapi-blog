from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from models import post_model
from database.database import engine
from routers import posts_routes

app = FastAPI()

app.include_router(posts_routes.router)

post_model.Base.metadata.create_all(engine)

# Static access
app.mount("/images", StaticFiles(directory="images"), name="images")

# CORS Error
origins = [
    "https://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
