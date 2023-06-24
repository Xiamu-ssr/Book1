# %%
from pyhive import hive
import pandas as pd
import numpy as np
from TCLIService.ttypes import TOperationState
from tqdm import tqdm

conn = hive.connect('127.0.0.1', port=10000, username='hive', database="sky")
cursor = conn.cursor()

# %%
def single_cmd(cmd:str):
    pbar = tqdm(total=100)
    cursor.execute(cmd, async_=True)
    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
        progress = cursor.poll().progressUpdateResponse.progressedPercentage
        pbar.update(int(progress * 100) - pbar.n)
        status = cursor.poll().operationState
    results = None
    try:results = cursor.fetchall()
    except Exception as e:
        pass
    pbar.close()
    if results:
        return pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
    else:
        return None

# %%

res = pd.DataFrame({})
for t in ['pv', 'cart', 'fav', 'buy']:
    tmp = single_cmd('''select item_id,
                    count(*) as count 
                    from user_behavior1
                    where behavior_type='{}'
                    group by item_id
                    order by count desc
                    limit 50
                    '''.format(t))
    # print(tmp.head())
    res[t] = [{k:v} for k,v in zip(tmp['item_id'], tmp['count'])]

# %%
single_cmd('''CREATE TABLE IF NOT EXISTS res_item_rank (
                `rank` int ,
                `pv` string ,
                `cart` string ,
                `fav` string ,
                `buy` string )
                row format delimited
                fields terminated by ','
                lines terminated by '\n'
                STORED AS TEXTFILE
            ''')

# %%
def multi_insert(table:str, values:list):
    cmd = "INSERT INTO " + table + " VALUES "
    for i in values:
        cmd += '("{}", "{}", "{}", "{}", "{}")'.format(i[0], i[1], i[2], i[3], i[4]) + ", "
    cmd = cmd[:-2]
    print(cmd)
    single_cmd(cmd)

# %%
res = res.astype(str)
res['rank'] = res.index
res['rank'] = res['rank'] + 1
res = res.reindex(columns=['rank', 'pv', 'cart', 'fav', 'buy'])
res = res.to_numpy()
print(res)

# %%
multi_insert("res_item_rank", res)

# %%
print(single_cmd('''select * from res_item_rank'''))

# %%
cursor.close()
conn.close()


