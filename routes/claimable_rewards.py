from aws_utils import dynamodb, get_metadata_table, get_claimable_table
from boto3.dynamodb.conditions import Key
from typing import Dict

MAX_BLOCK = 1000000000000
def get_claimable_metadata(chain) -> str:
    kce = Key("chain").eq(chain) & Key("startBlock").between(0, MAX_BLOCK)
    table = dynamodb.Table(get_metadata_table())
    try:
        output = table.query(
            IndexName="IndexMetadataChainAndStartBlock",
            KeyConditionExpression=kce,
            ScanIndexForward=False,
            Limit=1,
        )
        return output["Items"][0]["chainStartBlock"]
    except Exception as e:
        return ""
    
def get_claimable_balance(chain, addr):
    table = dynamodb.Table(get_claimable_table())
    print(chain, addr)
    chain_start_block = get_claimable_metadata(chain)
    kce = Key("chainStartBlock").eq(chain_start_block) & Key("address").eq(addr)
    response = table.query(KeyConditionExpression=kce)
    data = response["Items"]
    return data
    
    
        
