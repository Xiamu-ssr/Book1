# TTV.py

> class TTV(data:torch\_geometric.data.Data, model:nn.Module, optimizer:torch.optim.Optimizer, criterion:nn.Module, epochs:int, wandbname: str=""):

TTV, train valid test类，用于简化训练代码。

**PARAMETERS**

* data(Tensor) - 数据，一般为一张图，包含了x，edge\_index，mask等等
* model(nn.Module) - 模型
* optimizer(torch.optim.Optimizer) - 优化器
* criterion(nn.Module) - 损失函数
* epochs(int) - 训练轮数
* wandbname(str) - wandb项目名称，为空时不上传wandb。

> train() -> None

训练，包含valid，无打印，会上传wandb，如果指定了wandbname。

> test() -> None

测试。打印acc。

> tocsv(name:str='GCN') -> None

把模型预测的节点信息保存到csv。名称为`name+_nodes.csv`，两列，第一列node\_id,第二列label。
