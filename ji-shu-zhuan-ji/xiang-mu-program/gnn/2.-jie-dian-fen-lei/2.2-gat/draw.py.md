# draw.py

> draw(edges:list, node:pandas.DataFrame, name:str) -> None

使用graph-tools作图，保存为pdf

**PARAMETERS**

* edges(list) - 一个元组列表，每个元素为一对，表示一条有向边。不过这个函数默认为有向边。
* node(pandas.DataFrame) - 两列，第一列为node\_id，第二列为label。使用数据集的tocsv()默认为这样的列名。
* name(str) - 保存文件名，name+\_graph.pdf
