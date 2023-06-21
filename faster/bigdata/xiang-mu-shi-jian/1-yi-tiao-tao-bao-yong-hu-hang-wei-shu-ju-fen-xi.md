# 1 亿条淘宝用户行为数据分析

## 1. 部署环境

环境采用本地Winodws+VMware虚拟化部署基于Ambari的Hadoop集群。

集群配置如下

|           | namenode \* 1      | datanode \* 3      |
| --------- | ------------------ | ------------------ |
| i5-12450H | 2 core \* 1 thread | 2 core \* 1 thread |
| Memory    | 12GB               | 12GB               |
| Disk      | 150GB              | 100GB              |

集群安装的hadoop生态组件如下q

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
create table user_behavior (
`user_id` string comment 'user ID',
`item_id` string comment 'item ID',
`category_id` string comment 'category ID',
`behavior_type` string  comment 'behavior type among pv, buy, cart, fav',
`timestamp` int comment 'timestamp')
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
```

{% hint style="info" %}
这里使用以列优先的存储格式，定义压缩算法为snappy，对于像电商分析这样主要查询列的项目，会提高很多效率。
{% endhint %}

将数据导入到ORC表中，hive会自动执行 行列转化

```sql
insert into table user_behavior select * from temp_user_behavior;
```

查看一共多少条数据。

```
select count(*) from user_behavior;
+------------+
|    _c0     |
+------------+
| 100150807  |
+------------+
```

### 2.2 数据清洗

<pre class="language-sql"><code class="lang-sql">-- 确定2017-11-25 和 2017-12-03的时间戳
SELECT unix_timestamp('2017-11-25', 'yyyy-MM-dd');
+-------------+
|     _c0     |
+-------------+
| 1511568000  |
+-------------+
SELECT unix_timestamp('2017-12-03 23:59:59');
+-------------+
|     _c0     |
+-------------+
| 1512345599  |
+-------------+

select date(datetime) as day, COUNT(*) from user_behavior group by date(datetime) order by day;

<strong>-- 删除不在2017-11-25 到 2017-12-03日期的数据
</strong>insert overwrite table user_behavior
select user_id, item_id, category_id, behavior_type, `timestamp`
from user_behavior
where datetime between 1511568000 and 1512345599;

-- 再次查看时间是否有异常值
select date(datetime) as day, COUNT(*) from user_behavior group by date(datetime) order by day;

+-------------+-----------+
|     _c0     |    day    |
+-------------+-----------+
| 2017-11-28  | 9884185   |
| 2017-11-27  | 10013455  |
| 2017-11-29  | 10319060  |
| 2017-11-25  | 10511597  |
| 2017-11-30  | 10541695  |
| 2017-11-26  | 10571039  |
| 2017-12-01  | 11171505  |
| 2017-12-03  | 11961006  |
| 2017-12-02  | 13940942  |
+-------------+-----------+
</code></pre>

```sql
--数据清洗，时间戳格式化成 datetime
insert overwrite table user_behavior
select user_id, item_id, category_id, behavior_type, `timestamp`, from_unixtime(`timestamp`, 'yyyy-MM-dd HH:mm:ss')
from user_behavior;

-- check一下
select * from user_behavior limit 10;
+------------------------+------------------------+----------------------------+------------------------------+--------------------------+-------------------------+
| user_behavior.user_id  | user_behavior.item_id  | user_behavior.category_id  | user_behavior.behavior_type  | user_behavior.timestamp  | user_behavior.datetime  |
+------------------------+------------------------+----------------------------+------------------------------+--------------------------+-------------------------+
| 1                      | 1305059                | 2520771                    | pv                           | 1511911930               | 2017-11-28 23:32:10     |
| 1                      | 1323189                | 3524510                    | pv                           | 1512149435               | 2017-12-01 17:30:35     |
| 1                      | 1338525                | 149192                     | pv                           | 1511773214               | 2017-11-27 09:00:14     |
| 1                      | 1340922                | 4690421                    | pv                           | 1512041260               | 2017-11-30 11:27:40     |
| 1                      | 1531036                | 2920476                    | pv                           | 1511733732               | 2017-11-26 22:02:12     |
| 1                      | 2028434                | 4801426                    | pv                           | 1512224248               | 2017-12-02 14:17:28     |
| 1                      | 2041056                | 4801426                    | pv                           | 1512187543               | 2017-12-02 04:05:43     |
| 1                      | 2087357                | 2131531                    | pv                           | 1511975142               | 2017-11-29 17:05:42     |
| 1                      | 2087357                | 2131531                    | pv                           | 1512004568               | 2017-11-30 01:16:08     |
| 1                      | 2104483                | 4756105                    | pv                           | 1512194830               | 2017-12-02 06:07:10     |
+------------------------+------------------------+----------------------------+------------------------------+--------------------------+-------------------------
```

{% hint style="info" %}
Q:为什么不能是select date(datetime) as day from user\_behavior group by day  order by day;

A:在 SQL 查询中，`SELECT` 子句中定义的别名或计算字段并不能直接在 `GROUP BY` 子句中使用，因为 `GROUP BY` 子句是在 `SELECT` 子句之后执行的。也就是说，在查询执行过程中，`GROUP BY` 子句并不知道 `SELECT` 子句中定义的别名或计算字段，因此需要在 `GROUP BY` 子句中使用实际的列名或表达式。
{% endhint %}

```sql
--查看 behavior_type 是否有异常值
select behavior_type, COUNT(*) from user_behavior group by behavior_type;

+----------------+-----------+
| behavior_type  |    _c1    |
+----------------+-----------+
| cart           | 5466118   |
| pv             | 88596886  |
| buy            | 1998944   |
| fav            | 2852536   |
+----------------+-----------+
```

### 2.3 表分区

```sql
create table user_behavior (
`user_id` string comment 'user ID',
`item_id` string comment 'item ID',
`category_id` string comment 'category ID',
`behavior_type` string  comment 'behavior type among pv, buy, cart, fav',
`timestamp` int comment 'timestamp',
`datetime` string comment 'date')
parition ()
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");
```

```sql
-- 去掉完全重复的数据
insert overwrite table user_behavior
select user_id, item_id, category_id, behavior_type, `timestamp`, `datetime`
from user_behavior
group by user_id, item_id, category_id, behavior_type, `timestamp`, `datetime`;

-- 查看目前多少条
select count(*) from user_behavior;
+------------+
|    _c0     |
+------------+
| 100150758  |
+------------+
```

{% hint style="info" %}
在Hadoop MapReduce中，`GROUP BY` 操作通常是在Reduce端完成的，因为需要将具有相同key的记录汇总到一起进行聚合计算。由于Reduce端需要处理大量的数据，因此在处理大数据集时，可能会导致Reduce阶段的运行时间过长，影响整个作业的性能。

为了提高MapReduce作业的性能，可以采用以下方法：

1. 增加Reduce任务的数量：通过增加Reduce任务的数量，可以将数据均匀地分配到多个Reduce任务中，从而减少每个Reduce任务需要处理的数据量，提高作业的运行效率。

```sql
set mapreduce.job.reduces = 10;
```

2. 使用Combiner函数：Combiner函数可以在Map端进行数据聚合，从而减少Reduce端需要处理的数据量。Combiner函数可以执行一些简单的聚合操作，如求和、计数、求最大值或最小值等。

```sql
set hive.map.aggr=true;
INSERT OVERWRITE TABLE user_behavior
SELECT user_id, item_id, category_id, behavior_type, `timestamp`, `datetime`, COUNT(*)
FROM user_behavior
GROUP BY user_id, item_id, category_id, behavior_type, `timestamp`, `datetime`
;
```
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

