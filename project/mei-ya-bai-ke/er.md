# 二

从三元组构建知识图谱



### 实体对齐

多个节点可以是同一实体，比如通过相似度计算

### 实体消歧

同一名称但代指不同实体

### 属性对齐

### 知识推理

A-儿子-B，B-儿子-C，则推测A-孙子-C

知识表示

将知识图谱中的实体，关系，属性等转化为向量



## 一、环境配置

使用neo4j

{% embed url="https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-service-start-automatically" %}

`sudo vim /etc/neo4j/neo4j.conf`修改ip 0.0.0.0 和port 5173
