from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from routes.boost import get_boost
from routes.claimable_rewards import get_claimable_balance
from routes.cycle_data import get_rewards_data


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
def boost(chain: str = "ethereum"):
    return get_boost(chain)



@app.get("/claimable/{addr}")
def cycle(addr: str, chain: str = "ethereum"):
    return get_claimable_balance(chain, addr)

@app.get("/cycle/{cycle}")
def cycle(cycle: str, chain: str = "ethereum"):
    return get_rewards_data(chain, cycle)
