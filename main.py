from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from routes.boost import get_boost
from routes.scores import get_score_of_address
from routes.cycles import paginate_cycles,fill_latest_cycles, get_cycle
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/boosts")
def boost():
    return get_boost()

@app.get('/scores/{address}')
def scores(address: str):
    return get_score_of_address(address)

@app.get('/cycles/{page}')
def cycles(page: int):
    return paginate_cycles(page)

@app.get('/cycle/{number}')
def cycle(number: int):
    return get_cycle(number)

@app.on_event("startup")
@repeat_every(seconds=30)
def periodic():
    fill_latest_cycles()
