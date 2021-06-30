from aws_utils import fetch_scores

scores = {}

conditions = {
    "cond1":"Badger Staking & LPing",
    "cond2":"Digg Staking & LPing",
    "cond3":"Badger Governance Participant",
    "cond4": "Badger NFT owner",
    "cond5": "Non-native sett user",
    "cond6": "ibBTC sett user"
}
def get_scores():
    global scores
    if len(scores) == 0:
        scores = fetch_scores()
    return scores

def get_score_of_address(address):
    sc = get_scores()
    data = sc.get(address,{})
    return {
        "success": len(data) > 0,
        "data": data,
        "conditions": conditions
    }