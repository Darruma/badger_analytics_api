from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from routes.boost import get_boost
from routes.scores import get_score_of_address
from routes.cycles import paginate_cycles, fill_latest_cycles, get_cycle
from routes.unlock_schedules import get_schedules
from routes.nfts import get_nfts, get_user_nfts


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


@app.get("/schedules")
def schedules(chain: str = "ethereum"):
    return get_schedules(chain)


@app.get("nfts")
def nfts():
    return get_nfts()


@app.get("/nft_score/{address}")
def nft_score(address: str):
    return get_user_nfts(address)


@app.get("/scores/{address}")
def scores(address: str):
    return get_score_of_address(address)


@app.get("/cycles")
def cycles(chain: str, limit: int, offset: Optional[int] = 0):
    print(offset)
    return paginate_cycles(chain, limit, offset)


@app.get("/cycle/{number}")
def cycle(number: int, chain: str = "ethereum"):
    return get_cycle(number, chain)


@app.on_event("startup")
@repeat_every(seconds=120)
def periodic():
    fill_latest_cycles("ethereum")
    fill_latest_cycles("polygon")
    fill_latest_cycles("arbitrum")
