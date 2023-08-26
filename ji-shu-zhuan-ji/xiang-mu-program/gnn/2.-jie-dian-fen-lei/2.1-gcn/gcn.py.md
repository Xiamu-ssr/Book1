# GCN.py

> Class GCN(in\_channels:int, hidden\_channels:list, out\_channels:int, dropout:float=0.0)

GCN模型

**PARAMETERS**

* in\_channels(int) - 输入层节点数，一般等于特征数。
* hidden\_channels(list) - 隐藏层列表
* out\_channels(int) - 输出层节点数，一般等于类别数。
* dropout(float) - 模型dropout率

> forward(x:tg.data.Data.x, edge\_index:tg.data.Data.edge\_index) -> Tensor

**PARAMETERS**

* x(Tensor) - 节点特征张量，一般为二维张量，第一维表示节点，第二维表示某节点特征。
* edge\_index(Tensor) - 边张量，一般为2行e列，e为边数，2行对应列元素表示一条有向边。
