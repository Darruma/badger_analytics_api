import json, sys
from pool import db
from aws_utils import list_all_cycles, fetch_cycle

create_table_query = """
create table if not exists cycle_table(
        cycle int not null,
        merkleroot varchar(100) not null,
        contentHash varchar(100) not null,
        startBlock int not null,
        endBlock int not null,
        totalTokenDist json,
        primary key (cycle)
    );
"""
def check_for_cycle(cycleNumber):
    check_cycle_query = """
        select exists(select 1 from cycle_table where cycle=%s)
    """
    with db() as (conn,cur):
        cur.execute(check_cycle_query,(cycleNumber,))
        return cur.fetchone()[0]


def fill_latest_cycles():
    cycles = list_all_cycles()
    print(cycles)
    for cycle in cycles:
        if not check_for_cycle(cycle):
            print("Fetching cycle {}".format(cycle))
            cycle_data = fetch_cycle(cycle)
            print("Fetched cycle data")
            print(cycle_data)
            print(len(cycle_data))
            add_cycle_to_db(cycle_data)
            print("added")

def add_cycle_to_db(cycle):
    print("adding cycle {} to db".format(cycle["cycle"]))
    cycle = {k.lower(): v for k, v in cycle.items()}
    with db() as (conn,cur):
        cur.execute(create_table_query)
        insert_query = """
        insert into cycle_table
            select * from json_populate_record(NULL::cycle_table, %s) 
        """
        print("executing query")
        cur.execute(insert_query,(json.dumps(cycle),))
        conn.commit()


def paginate_cycles(page):
    records_per_page = 5;
    offset = (int(page+1) - 1) * records_per_page
    paginate_query = """
    select * from cycle_table 
    order by cycle
    limit (%s)
    offset (%s)
    """
    cycle_data = []
    with db() as (conn,cur):
        cur.execute(paginate_query,(records_per_page,offset))
        result = cur.fetchall()
        for data in result:
            cycle_data.append({
                "cycle":data[0],
                "merkleRoot":data[1],
                "contentHash":data[2],
                "startBlock": data[3],
                "endBlock": data[4],
                "totalTokenDist": data[5]
            })
    return cycle_data