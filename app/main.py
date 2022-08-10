from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# no longer necessary since alembic handles this now
# models.Base.metadata.create_all(bind=engine)

origins = ["*"] # and anyone can use it
# origins = ["https://www.google.com"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # only allow GET?
    allow_headers=["*"],    # only allow specific headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!!!!!!!!!!!!!!!!!"}
