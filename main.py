from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from boost import get_boost
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/boosts")
def read_root():
    return get_boost()


