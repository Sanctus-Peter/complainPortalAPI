from fastapi import FastAPI

from .database import engine
from .routers import auth, admin, user, view
from . import models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(view.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "complaint portal"}
