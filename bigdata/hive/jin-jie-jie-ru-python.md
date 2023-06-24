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

# 连接Hive
conn = hive.connect('127.0.0.1', port=10000, username='hive')

# 执行命令
cursor = conn.cursor()
cursor.execute('SHOW DATABASES')

# 获取结果
results = cursor.fetchall()

# 将结果转换为Pandas DataFrame
df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

# 打印结果
print(df)

# 关闭游标和连接
cursor.close()
conn.close()
```
