from typing import Optional
from fastapi import FastAPI
from boost import get_boost
app = FastAPI()


@app.get("/boosts")
def read_root():
    return get_boost()


