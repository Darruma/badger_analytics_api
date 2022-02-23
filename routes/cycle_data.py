from aws_utils import dynamodb, get_rewards_table
from boto3.dynamodb.conditions import Key

def get_rewards_data(chain: str, cycle: int):
    table = dynamodb.Table(get_rewards_table())
    network_cycle = f"{chain}-{cycle}"
    kce = Key("networkCycle").eq(network_cycle) 
    
    try:
        output = table.query(
            KeyConditionExpression=kce,
        )
        if len(output["Items"]):
            return output["Items"][0]
        return {}
        
    except Exception as e:
        return e
    