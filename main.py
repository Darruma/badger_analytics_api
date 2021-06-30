from scores import get_scores
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from boost import get_boost
from scores import get_score_of_address
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
def boost():
    return get_boost()


@app.get('/scores/{address}')
def scores(address):
    return get_score_of_address(address)