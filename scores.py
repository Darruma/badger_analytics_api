from aws_utils import fetch_scores

scores = {}

def get_scores():
    global scores
    if len(scores) == 0:
        scores = fetch_scores()
    return scores