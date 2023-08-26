# Cora.py

> **class Cora(device:str)**

只有一张无向图

<table data-header-hidden><thead><tr><th width="167"></th><th width="121"></th><th width="113"></th><th width="118"></th><th></th></tr></thead><tbody><tr><td>Name</td><td>#nodes</td><td>#edges</td><td>#features</td><td>#classes</td></tr><tr><td>Cora</td><td>2,708</td><td>10,556</td><td>1,433</td><td>7</td></tr></tbody></table>

#### PARAMETERS

* device(str) - 指定设备，cpu或者cuda，作用于cora的唯一一张图。

> **printInfo() -> None**

打印Cora数据集常用属性。

> **tocsv(name:str) -> None**

将cora唯一一张图保存到csv，一个为`name+_nodes.csv`，两列，分别为node id和node class；一个为`name+_edges.csv`,两列，分别为source和target，其实没分别，因为cora数无向图。

#### PARAMETERS

* name(str) - 指定csv文件前缀名称。
