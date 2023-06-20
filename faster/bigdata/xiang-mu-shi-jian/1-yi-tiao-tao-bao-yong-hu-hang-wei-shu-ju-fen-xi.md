# 1 亿条淘宝用户行为数据分析

## 1. 部署环境

环境采用本地Winodws+VMware虚拟化部署基于Ambari的Hadoop集群。

集群配置如下

|           | namenode \* 1      | datanode \* 3      |
| --------- | ------------------ | ------------------ |
| i5-12450H | 2 core \* 1 thread | 1 core \* 1 thread |
| Memory    | 12GB               | 12GB               |
| Disk      | 150GB              | 100GB              |

集群安装的hadoop生态组件如下

| HDFS           | 3.1.1.3.1         |
| -------------- | ----------------- |
| YARN           | 3.1.1             |
| MapReduce2     | 3.1.1             |
| Tez            | 0.9.1             |
| Hive           | 3.1.0             |
| HBase          | 2.0.2             |
| ZooKeeper      | 3.4.6             |
| Ambari Metrics | 0.1.0             |
| SmartSense     | 1.5.1.2.7.4.0-118 |

## 2. 数据集下载

{% embed url="https://pan.baidu.com/s/1CPD5jpmvOUvg1LETAVETGw" %}
提取码：m4mc
{% endembed %}

这是一份来自淘宝的用户行为数据，时间区间为 2017-11-25 到 2017-12-03，总计 100,150,807 条记录，大小为 3.5 G，包含 5 个字段。

|                     |                                            |
| ------------------- | ------------------------------------------ |
| 用户ID（User ID）       | 一个整数                                       |
| 商品ID（Item ID）       | 一个整数                                       |
| 类别ID（Category ID）   | 一个整数                                       |
| 行为类型（Behavior Type） | “pv”（浏览）、“buy”（购买）、“cart”（加入购物车）、“fav”（收藏） |
| 时间戳（Timestamp）      | 一个整数，通常以秒为单位。                              |

## 3. 数据处理

### 2.1 数据导入

`beeline -n hive -p`进入hql命令行

```sql
-- 建表
drop table if exists user_behavior;
create table user_behavior (
`user_id` string comment 'user ID',
`item_id` string comment 'item ID',
`category_id` string comment 'category ID',
`behavior_type` string  comment 'behavior type among pv, buy, cart, fav',
`timestamp` int comment 'timestamp',
`datetime` string comment 'date')
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile;

-- 加载数据
LOAD DATA LOCAL INPATH '/root/Hive/UserBehavior.csv' OVERWRITE INTO TABLE user_behavior ;
```

一共有100150807条数据

```
select count(*) from user_behavior;
+------------+
|    _c0     |
+------------+
| 100150807  |
+------------+
```

### 2.2 数据清洗

```sql
-- 去掉完全重复的数据
insert overwrite table user_behavior
select user_id, item_id, category_id, behavior_type, timestamp, datetime
from user_behavior
group by user_id, item_id, category_id, behavior_type, timestamp, datetime;
```
