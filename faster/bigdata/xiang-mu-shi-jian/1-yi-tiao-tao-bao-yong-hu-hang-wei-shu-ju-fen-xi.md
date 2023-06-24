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
select count(*) from user_behavior1;
+-----------+
|    _c0    |
+-----------+
| 98914484  |
+-----------+
```

{% hint style="info" %}
DISTRIBUTE BY `date`, `behavior_type`这个是用来指定数据分发的策略，它会根据分区键的值将数据分发到不同的reduce任务中，每个reduce任务只处理一个分区的数据。这样就可以在每个分区内部去重，而不需要到全局数据去比较，所以效率高很多。在hdfs上，表按照 `date`, `behavior_type`分区后，分区的文件夹数量= `date`分区数\* `behavior_type`分区数。当DISTRIBUTE BY `date`, `behavior_type`;时，可以理解为是在`date`分区数\* `behavior_type`分区数 这么多个局部中比较去重。

同时如果DISTRIBUTE BY `date`, `behavior_type`粒度划分的太细，导致启动的容器太多，计算时间占比较低，可以选择只DISTRIBUTE BY一个。
{% endhint %}

## 3.数据分析可视化

### 3.1 基于时间的用户行为分析

#### 3.1.1 总访问量PV，总用户量UV

<pre class="language-sql"><code class="lang-sql">--总访问量PV，总用户量UV
create table res_pv_uv
comment "page views and unique visitor"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select pv, uv
from (
    select count(*) as pv from user_behavior1 where behavior_type='pv'
) t1
join(
<strong>    select count(distinct user_id) as uv from user_behavior1
</strong><strong>) t2
</strong><strong>on 1=1;
</strong>
select * from res_pv_uv;
+-----------+---------+
|    pv     |   uv    |
+-----------+---------+
| 88596886  | 987984  |
+-----------+---------+
</code></pre>

{% hint style="info" %}
思考以下select语句的优劣和正确性，和上面的语句谁能更好的发挥分区表的优势

{% code lineNumbers="true" %}
```sql
select sum(pv) as pv, count(distinct uv) as uv from (
    select count(*) as pv, distinct user_id as uv from user_behavior1 where behavior_type='pv'
    union all
    select 0 as pv, distinct user_id as uv from user_behavior1 where behavior_type='buy'
    union all
    select 0 as pv, distinct user_id as uv from user_behavior1 where behavior_type='cart'
    union all
    select 0 as pv, distinct user_id as uv from user_behavior1 where behavior_type='fav'
) t;

```
{% endcode %}

{% code lineNumbers="true" %}
```sql
select sum(case when behavior_type = 'pv' then 1 else 0 end) as pv,
       count(distinct user_id) as uv
from user_behavior1;
```
{% endcode %}
{% endhint %}

#### 3.1.2 日均访问量，日均用户量

<pre class="language-sql"><code class="lang-sql">--日均访问量，日均用户量
<strong>create table res_pv_uv_per_day
</strong>comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select t1.`date` as `date`, pv, uv
from(
    select `date`, count(*) as pv from user_behavior1 group by `date` order by `date`
) t1
join(
    select `date`, count(distinct user_id) as uv from user_behavior1 group by `date` order by `date`
) t2
on t1.`date`=t2.`date`
order by `date`;

+--------------------------+------------------------+------------------------+
| res_pv_uv_per_day1.date  | res_pv_uv_per_day1.pv  | res_pv_uv_per_day1.uv  |
+--------------------------+------------------------+------------------------+
| 2017-11-25               | 10511597               | 705571                 |
| 2017-11-26               | 10571039               | 713522                 |
| 2017-11-27               | 10013455               | 709207                 |
| 2017-11-28               | 9884185                | 708339                 |
| 2017-11-29               | 10319060               | 719356                 |
| 2017-11-30               | 10541695               | 730809                 |
| 2017-12-01               | 11171505               | 753166                 |
| 2017-12-02               | 13940942               | 941709                 |
| 2017-12-03               | 11961006               | 917531                 |
+--------------------------+------------------------+------------------------+
</code></pre>

#### 3.1.3 一天的活跃时段分布

```sql
-- 一天的活跃时段分布
create table res_behavior_among_day
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select t.hour as hour,
       collect_list(map(t.behavior_type, t.count)) as tc
from(
SELECT hour(`timestamp`) AS hour, 
       behavior_type, 
       COUNT(*) AS count
FROM user_behavior1
GROUP BY behavior_type, hour(`timestamp`)
) t
group by hour
order by hour;
 
 +---------+----------------------------------------------------+
| hour    |                        tc                          |
+---------+----------------------------------------------------+
| 0       | [{"buy":64916},{"cart":192036},{"fav":103721},{"pv":3042342}] |
| 1       | [{"buy":96134},{"cart":229890},{"fav":127976},{"pv":3728498}] |
| 2       | [{"buy":127932},{"cart":266963},{"fav":147752},{"pv":4334810}] |
| 3       | [{"buy":122046},{"cart":260831},{"fav":145412},{"pv":4213518}] |
| 4       | [{"buy":118591},{"cart":255811},{"fav":140862},{"pv":4255794}] |
| 5       | [{"buy":123426},{"cart":279829},{"fav":150844},{"pv":4653933}] |
| 6       | [{"buy":122171},{"cart":277093},{"fav":148561},{"pv":4642054}] |
| 7       | [{"buy":122728},{"cart":284269},{"fav":151321},{"pv":4806704}] |
| 8       | [{"buy":116444},{"cart":279035},{"fav":148722},{"pv":4607743}] |
| 9       | [{"buy":101300},{"cart":255342},{"fav":137631},{"pv":4203395}] |
| 10      | [{"buy":95907},{"cart":253193},{"fav":133262},{"pv":4313516}] |
| 11      | [{"buy":115032},{"cart":314774},{"fav":161057},{"pv":5430878}] |
| 12      | [{"buy":133859},{"cart":393209},{"fav":191406},{"pv":6586331}] |
| 13      | [{"buy":145431},{"cart":465924},{"fav":219974},{"pv":7538382}] |
| 14      | [{"buy":138263},{"cart":486249},{"fav":232222},{"pv":7443069}] |
| 15      | [{"buy":100070},{"cart":395920},{"fav":195330},{"pv":5599901}] |
| 16      | [{"buy":52422},{"cart":164776},{"fav":94930},{"pv":2747149}] |
| 17      | [{"buy":20948},{"cart":76954},{"fav":46239},{"pv":1278813}] |
| 18      | [{"buy":10748},{"cart":41541},{"fav":25079},{"pv":692240}] |
| 19      | [{"buy":7212},{"cart":29333},{"fav":16791},{"pv":471981}] |
| 20      | [{"buy":6044},{"cart":25564},{"fav":13260},{"pv":403765}] |
| 21      | [{"buy":7351},{"cart":33462},{"fav":17158},{"pv":522063}] |
| 22      | [{"buy":16251},{"cart":73014},{"fav":36388},{"pv":1097628}] |
| 23      | [{"buy":33718},{"cart":131106},{"fav":66638},{"pv":1982379}] |
+---------+----------------------------------------------------+
```

{% hint style="info" %}
比较以下语句

{% code lineNumbers="true" %}
```sql
select hour(`timestamp`) as hour,
       sum(case when behavior_type = 'pv' then 1 else 0 end) as pv,   --点击数
       sum(case when behavior_type = 'fav' then 1 else 0 end) as fav,  --收藏数
       sum(case when behavior_type = 'cart' then 1 else 0 end) as cart,  --加购物车数
       sum(case when behavior_type = 'buy' then 1 else 0 end) as buy  --购买数
from user_behavior1
group by hour(`timestamp`)
order by hour;
```
{% endcode %}
{% endhint %}

#### 3.1.4 一周用户的活跃分布

```sql
--一周用户的活跃分布
create table res_behavior_among_week
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select t1.weekday as weekday ,
       collect_list(map(t1.behavior_type ,
       (case when weekday=6 then ceil(t1.count/2)
              when weekday=7 then ceil(t1.count/2)
              else t1.count end)
       )) as ct
from(
       select pmod(datediff(t.d, '2017-11-25')+5, 7)+1 as weekday,
              t.behavior_type as behavior_type ,
              sum(t.count) as count
       from (
              select `date` as d,
                     behavior_type,
                     COUNT(*) as count
              from user_behavior1
              group by behavior_type , `date`
       ) t
       group by pmod(datediff(t.d, '2017-11-25')+5, 7)+1, t.behavior_type
       order by weekday
) t1
group by t1.weekday
order by weekday;

+----------+----------------------------------------------------+
| weekday  |                         tc                         |
+----------+----------------------------------------------------+
| 1        | [{"buy":218401},{"cart":539212},{"fav":289413},{"pv":8966429}] |
| 2        | [{"buy":211754},{"cart":533807},{"fav":289431},{"pv":8849193}] |
| 3        | [{"buy":223077},{"cart":554747},{"fav":299588},{"pv":9241648}] |
| 4        | [{"buy":222235},{"cart":573032},{"fav":304428},{"pv":9442000}] |
| 5        | [{"buy":212849},{"cart":642251},{"fav":314121},{"pv":10002284}] |
| 6        | [{"buy":230424},{"cart":685302},{"fav":355318},{"pv":10955227}] |
| 7        | [{"buy":224891},{"cart":626233},{"fav":322460},{"pv":10092439}] |
+----------+----------------------------------------------------+
```

{% hint style="info" %}
比较以下语句

{% code lineNumbers="true" %}
```sql
select pmod(datediff(`date`, '2017-11-25') + 5, 7)+1 as weekday,
       sum(case when behavior_type = 'pv' then 1 else 0 end) as pv,   --点击数
       sum(case when behavior_type = 'fav' then 1 else 0 end) as fav,  --收藏数
       sum(case when behavior_type = 'cart' then 1 else 0 end) as cart,  --加购物车数
       sum(case when behavior_type = 'buy' then 1 else 0 end) as buy  --购买数
from user_behavior1
group by pmod(datediff(`date`, '2017-11-25')+5, 7)+1
order by weekday;
```
{% endcode %}

{% code lineNumbers="true" %}
```sql
select t.weekday as weekday,
       collect_list(map(t.behavior_type, 
              (case when weekday=6 then ceil(t.count/2)
              when weekday=7 then ceil(t.count/2)
              else t.count end)
       )) as tc
from (
select pmod(datediff(`date`, '2017-11-25')+5, 7)+1 as weekday,
       behavior_type,
       COUNT(*) as count
from user_behavior1
group by behavior_type , pmod(datediff(`date`, '2017-11-25')+5, 7)+1
) t
group by weekday
order by weekday;
```
{% endcode %}
{% endhint %}

### 3.2 用户行为转换率

```sql
--点击/(加购物车+收藏)/购买 , 各环节转化率
create table res_conversion_rate
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select pv, fav, cart, fav_cart, buy,
       round(fav_cart/pv, 4) as pv2favcart,
       round(buy/fav_cart, 4) as favcart2buy,
       round(buy/pv, 4) as pv2buy
from(
       select cast(gm['pv'] as int) as pv,
              cast(gm['fav'] as int) as fav,
              cast(gm['cart'] as int) as cart,
              cast(gm['fav']+gm['cart'] as int) as fav_cart,
              cast(gm['buy'] as int) as buy
       from(
              select collect(cast(behavior_type as string), cast(count as string)) as gm
              from(
                     select behavior_type,
                            COUNT(*) as count
                     from user_behavior1
                     group by behavior_type
              )t1
       ) t2
) t3;

+-----------+----------+----------+------------+----------+-------------+--------------+---------+
|    pv     |   fav    |   cart   |  fav_cart  |   buy    | pv2favcart  | favcart2buy  | pv2buy  |
+-----------+----------+----------+------------+----------+-------------+--------------+---------+
| 88596886  | 2852536  | 5466118  | 8318654.0  | 1998944  | 0.0939      | 0.2403       | 0.0226  |
+-----------+----------+----------+------------+----------+-------------+--------------+---------+
```

{% hint style="info" %}
这里使用了Brickhouse UDF，用collect UDF便捷实现了TRANSPOSE
{% endhint %}

### 3.3 复购率

```sql
--每个用户的购物情况，加工到 user_behavior_count
create table res_doublebuy_rate
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select round(t2.count/uv,6) as rate
from(
    select count(*) as count
    from(
        select count(*) as count
        from user_behavior1
        where behavior_type='buy'
        group by user_id
    ) t1
    where t1.count>1
) t2
join(
    select uv from res_pv_uv
) t3;

+--------------------------+
| res_doublebuy_rate.rate  |
+--------------------------+
| 0.446562                 |
+--------------------------+
```

### 3.4 基于 RFM 模型找出有价值的用户

RFM 模型是衡量客户价值和客户创利能力的重要工具和手段，其中由3个要素构成了数据分析最好的指标，分别是：

* R-Recency（最近一次购买时间）
* F-Frequency（消费频率）
* ~~M-Money（消费金额）~~

```sql
-- 创建一个临时表，记录每个用户的R-F排名
create temporary table temp_cte
as
select user_id,
       datediff('2017-12-04', max(`date`)) as R,
       dense_rank() over(order by datediff('2017-12-04', max(`date`))) as R_rank,
       count(*) as F,
       dense_rank() over(order by count(*) desc) as F_rank
from user_behavior1
where behavior_type = 'buy'
group by user_id;

+--------------+--------+-------------+--------+-------------+
| cte.user_id  | cte.r  | cte.r_rank  | cte.f  | cte.f_rank  |
+--------------+--------+-------------+--------+-------------+
| 486458       | 1      | 1           | 262    | 1           |
| 866670       | 2      | 2           | 175    | 2           |
| 702034       | 1      | 1           | 159    | 3           |
| 107013       | 1      | 1           | 130    | 4           |
| 1014116      | 1      | 1           | 118    | 5           |
| 432739       | 1      | 1           | 112    | 6           |
| 500355       | 4      | 4           | 110    | 7           |
| 537150       | 1      | 1           | 109    | 8           |
| 1003412      | 1      | 1           | 100    | 9           |
| 919666       | 1      | 1           | 97     | 10          |
+--------------+--------+-------------+--------+-------------+
```

```sql
-- R-F按照5-15个等级划分，因为本人认为value-F > value-R，然后计算每个用户的价值score
create table res_user_score
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select user_id, R, R_rank, R_score, F, F_rank, F_score,  R_score + F_score AS score
from(
select *,
       ntile(5) over(order by R_rank desc) as R_score,
       ntile(15) over(order by F_rank desc) as F_score
from temp_cte
) t
order by score desc;

+-------------------------+-------------------+------------------------+-------------------------+-------------------+------------------------+-------------------------+-----------------------+
| res_user_score.user_id  | res_user_score.r  | res_user_score.r_rank  | res_user_score.r_score  | res_user_score.f  | res_user_score.f_rank  | res_user_score.f_score  | res_user_score.score  |
+-------------------------+-------------------+------------------------+-------------------------+-------------------+------------------------+-------------------------+-----------------------+
| 180128                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 180131                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 935417                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 925900                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 590239                  | 1                 | 1                      | 5                       | 9                 | 79                     | 15                      | 20                    |
| 307773                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 856339                  | 1                 | 1                      | 5                       | 14                | 74                     | 15                      | 20                    |
| 178301                  | 1                 | 1                      | 5                       | 9                 | 79                     | 15                      | 20                    |
| 804543                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
| 327112                  | 1                 | 1                      | 5                       | 7                 | 81                     | 15                      | 20                    |
+-------------------------+-------------------+------------------------+-------------------------+-------------------+------------------------+-------------------------+-----------------------+
```

```sql
-- 计算每层价值用户有多少人
create table res_user_score_count
comment "page views and unique visitor each day"
row format delimited
fields terminated by ','
lines terminated by '\n'
STORED AS TEXTFILE
as
select score, count(*) as count 
from res_user_score 
group by score 
order by score desc;

+-----------------------------+-----------------------------+
| res_user_score_count.score  | res_user_score_count.count  |
+-----------------------------+-----------------------------+
| 20                          | 22104                       |
| 19                          | 22648                       |
| 18                          | 33199                       |
| 17                          | 31014                       |
| 16                          | 41697                       |
| 15                          | 32152                       |
| 14                          | 71802                       |
| 13                          | 34853                       |
| 12                          | 47973                       |
| 11                          | 20117                       |
| 10                          | 25696                       |
| 9                           | 36893                       |
| 8                           | 39444                       |
| 7                           | 63359                       |
| 6                           | 30289                       |
| 5                           | 29306                       |
| 4                           | 41855                       |
| 3                           | 36437                       |
| 2                           | 9532                        |
+-----------------------------+-----------------------------+
```

### 3.5 商品维度的分析

<pre class="language-sql"><code class="lang-sql"><strong>select item_id,
</strong>    count(*) as count
from user_behavior1
where behavior_type='buy'
group by item_id
order by count;
</code></pre>
