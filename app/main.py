from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database import engine
from .routers import auth, admin, user, view
from . import models


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(view.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "complaint portal"}
