# 进阶-接入Python

安装环境

```bash
yum install -y python3 pip3 python3-devel gcc cyrus-sasl-devel
pip3 install pyhive pandas
```

{% hint style="info" %}
遇到什么没有就装什么
{% endhint %}

一个简单的例子

```python
from pyhive import hive
import pandas as pd
from TCLIService.ttypes import TOperationState
from tqdm import tqdm

conn = hive.connect('127.0.0.1', port=10000, username='hive', database="sky")
cursor = conn.cursor()

def single_cmd(cmd:str):
    pbar = tqdm(total=100)
    cursor.execute(cmd, async_=True)
    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
        progress = cursor.poll().progressUpdateResponse.progressedPercentage
        pbar.update(int(progress * 100) - pbar.n)
        status = cursor.poll().operationState
    results = cursor.fetchall()
    pbar.close()
    df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
    return df
    
print(single_cmd('''select item_id,
                count(*) as count 
                from user_behavior1
                where behavior_type='buy'
                group by item_id
                order by count 
                limit 7
                 '''))
         
cursor.close()
conn.close()
```
