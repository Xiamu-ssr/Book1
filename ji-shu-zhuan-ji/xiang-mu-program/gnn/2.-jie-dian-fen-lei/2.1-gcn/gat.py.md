# GAT.py

> Class GCN(num\_features:int , num\_classes:int , hidden\_channels:list=\[8], num\_heads:list=\[8], dropout:float=0.6, attn\_dropout:float=0.6):

GAT模型

**PARAMETERS**

* num\_features(int) - 输入层节点数，一般等于特征数。
* num\_classes(int) - 输出层节点数，一般等于类别数。
* hidden\_channels(list) - 隐藏层列表
* num\_heads(list) - 注意头数量列表
* dropout(float) - 模型dropout率
* attn\_dropout(float) - 注意头dropout率

> forward(x:tg.data.Data.x, edge\_index:tg.data.Data.edge\_index) -> Tensor

**PARAMETERS**

* x(Tensor) - 节点特征张量，一般为二维张量，第一维表示节点，第二维表示某节点特征。
* edge\_index(Tensor) - 边张量，一般为2行e列，e为边数，2行对应列元素表示一条有向边。
