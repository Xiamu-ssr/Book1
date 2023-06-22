# 1 亿条淘宝用户行为数据分析

## 1. 部署环境

环境采用本地Winodws+VMware虚拟化部署基于Ambari的Hadoop集群。

集群配置如下

|           | namenode \* 1      | datanode \* 3      |
| --------- | ------------------ | ------------------ |
| i5-12450H | 2 core \* 1 thread | 2 core \* 1 thread |
| Memory    | 12GB               | 12GB               |
| Disk      | 150GB              | 100GB              |
| 额外软件包     | openJDK8、Mysql5.7  | openJDK8           |

集群安装的hadoop生态组件如下

|                |           |
| -------------- | --------- |
| HDFS           | 3.1.1.3.1 |
| YARN           | 3.1.1     |
| MapReduce2     | 3.1.1     |
| Tez            | 0.9.1     |
| Hive           | 3.1.0     |
| HBase          | 2.0.2     |
| ZooKeeper      | 3.4.6     |
| Ambari Metrics | 0.1.0     |

{% hint style="info" %}
**服务器调优**

关于YARN和总内存、总vcore和单个容器的内存、vocre分配需要自行选择合适的参数，尽量不浪费资源。
{% endhint %}

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

## 3. 数据处理和表优化

### 2.1 数据导入

`beeline -n hive -p`进入hql命令行

创建一个临时表，并加载csv数据文件加载到其中。

```sql
CREATE TEMPORARY TABLE temp_user_behavior (
`user_id` string comment 'user ID',
`item_id` string comment 'item ID',
`category_id` string comment 'category ID',
`behavior_type` string  comment 'behavior type among pv, buy, cart, fav',
`timestamp` int comment 'timestamp')
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '/root/Hive/UserBehavior.csv' OVERWRITE INTO TABLE temp_user_behavior ;
```

创建用户行为表1。

```sql
drop table if exists user_behavior1;
create table user_behavior1 (
`user_id` string comment 'user ID',
`item_id` string comment 'item ID',
`category_id` string comment 'category ID',
`timestamp` timestamp comment 'timestamp'
)
PARTITIONED BY (`date` date, `behavior_type` string comment 'behavior type among pv, buy, cart, fav')
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
```

{% hint style="info" %}
这里使用以列优先的存储格式，定义压缩算法为snappy，对于像电商分析这样主要查询列的项目，会提高很多效率。同时对日期date进行分区，以及用户行为behavior\_type进行分区是一种合理的分区方法，在后续分析过程中将大大提高查询速度。
{% endhint %}

将数据导入到ORC表中，hive会自动执行 行列转化

```sql
INSERT OVERWRITE TABLE user_behavior1 PARTITION (`date`, behavior_type)
SELECT
  user_id,
  item_id,
  category_id,
  from_unixtime(`timestamp`) AS `timestamp`,
  date(from_unixtime(`timestamp`)) AS `date`,
  behavior_type
FROM
  temp_user_behavior;
```

查看一共多少条数据。

```sql
select count(*) from user_behavior1;
+------------+
|    _c0     |
+------------+
| 100150807  |
+------------+
```

### 2.2 数据清洗

<pre class="language-sql"><code class="lang-sql"><strong>-- 查看时间-数据分布情况，是否有异常值
</strong>select `date`, COUNT(*) from user_behavior1 group by `date` order by `date`;

<strong>-- 删除不在2017-11-25 到 2017-12-03日期的数据
</strong>alter table user_behavior1 
drop IF EXISTS partition (`date`&#x3C;'2017-11-25'), partition (`date`>'2017-12-03');

-- 再次查看时间是否有异常值
select `date`, COUNT(*) from user_behavior1 group by `date` order by `date`;

+-------------+-----------+
|    date     |    _c1    |
+-------------+-----------+
| 2017-11-25  | 10511605  |
| 2017-11-26  | 10571046  |
| 2017-11-27  | 10013457  |
| 2017-11-28  | 9884189   |
| 2017-11-29  | 10319066  |
| 2017-11-30  | 10541698  |
| 2017-12-01  | 11171515  |
| 2017-12-02  | 13940949  |
| 2017-12-03  | 11961008  |
+-------------+-----------+
</code></pre>

```sql
--查看 behavior_type 是否有异常值
select behavior_type, COUNT(*) from user_behavior1 group by behavior_type;

+----------------+-----------+
| behavior_type  |    _c1    |
+----------------+-----------+
| cart           | 5466118   |
| pv             | 88596903  |
| buy            | 1998976   |
| fav            | 2852536   |
+----------------+-----------+
```

```sql
-- 去掉完全重复的数据
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE user_behavior1
PARTITION (`date`, `behavior_type`)
SELECT DISTINCT `user_id`, `item_id`, `category_id`, `timestamp`, `date`, `behavior_type`
FROM user_behavior1
DISTRIBUTE BY `date`, `behavior_type`;

-- 查看目前多少条
select count(*) from user_behavior;
+------------+
|    _c0     |
+------------+
| 100150758  |
+------------+
```

{% hint style="info" %}
DISTRIBUTE BY `date`, `behavior_type`这个是用来指定数据分发的策略，它会根据分区键的值将数据分发到不同的reduce任务中，每个reduce任务只处理一个分区的数据。这样就可以在每个分区内部去重，而不需要到全局数据去比较，所以效率高很多。在hdfs上，表按照 `date`, `behavior_type`分区后，分区的文件夹数量= `date`分区数\* `behavior_type`分区数。当DISTRIBUTE BY `date`, `behavior_type`;时，可以理解为是在`date`分区数\* `behavior_type`分区数 这么多个局部中比较去重。

同时如果DISTRIBUTE BY `date`, `behavior_type`粒度划分的太细，导致启动的容器太多，计算时间占比较低，可以选择只DISTRIBUTE BY一个。
{% endhint %}

## 3.数据分析可视化

### 3.1 用户流量及购物情况

```sql
--总访问量PV，总用户量UV
select sum(case when behavior_type = 'pv' then 1 else 0 end) as pv,
       count(distinct user_id) as uv
from user_behavior;

+-----------+---------+
|    pv     |   uv    |
+-----------+---------+
| 88596886  | 987984  |
+-----------+---------+
```

{% hint style="info" %}
Q : CASE WHEN除了上述的CASE WHEN THEN ELSE，还有什么用法

A :

1. 多重条件判断

{% code lineNumbers="true" %}
```sql
SELECT
  CASE
    WHEN score >= 90 THEN 'A'
    WHEN score >= 80 THEN 'B'
    ELSE 'C'
  END AS grade
FROM students;
```
{% endcode %}

2. 嵌套使用

{% code lineNumbers="true" %}
```sql
SELECT
  CASE
    WHEN score >= 90 THEN 'A'
    ELSE
      CASE
        WHEN score >= 80 THEN 'B'
        ELSE 'C'
      END
  END AS grade
FROM students;
```
{% endcode %}



3. 结合WHERE子句使用

{% code lineNumbers="true" %}
```sql
SELECT *
FROM students
WHERE
  CASE
    WHEN gender = 'male' THEN score >= 80
    WHEN gender = 'female' THEN score >= 90
    ELSE score >= 70
  END;
```
{% endcode %}

其中男生成绩大于等于80分，女生成绩大于等于90分，其他学生成绩大于等于70分
{% endhint %}

