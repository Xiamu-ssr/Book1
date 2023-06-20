# Hive常用DDL操作

## 一、Database

```sql
--显示所有数据库
show databases;
--使用指定数据库
USE database_name;
```

### 1.1 新建数据库

```
CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name   --DATABASE|SCHEMA 是等价的
  [COMMENT database_comment] --数据库注释
  [LOCATION hdfs_path] --存储在 HDFS 上的位置
  [WITH DBPROPERTIES (property_name=property_value, ...)]; --指定额外属性
```

```sql
CREATE DATABASE IF NOT EXISTS hive_test
  COMMENT 'hive database for test'
  WITH DBPROPERTIES ('create'='heibaiying');
```

### 1.2 查看数据库信息

```
DESC DATABASE [EXTENDED] db_name; --EXTENDED 表示是否显示额外属性
```

```sql
DESC DATABASE  EXTENDED hive_test;
```

### 1.3  删除数据库

```
DROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];
```

{% hint style="info" %}
默认行为是 RESTRICT，如果数据库中存在表则删除失败。要想删除库及其中的表，可以使用 CASCADE 级联删除。
{% endhint %}

```sql
DROP DATABASE IF EXISTS hive_test CASCADE;
```

## 二、创建表

### 2.1 建表语法

```
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name     --表名
  [(col_name data_type [COMMENT col_comment],
    ... [constraint_specification])]  --列名 列数据类型
  [COMMENT table_comment]   --表描述
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]  --分区表分区规则
  [
    CLUSTERED BY (col_name, col_name, ...) 
   [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS
  ]  --分桶表分桶规则
  [SKEWED BY (col_name, col_name, ...) ON ((col_value, col_value, ...), (col_value, col_value, ...), ...)  
   [STORED AS DIRECTORIES] 
  ]  --指定倾斜列和值
  [
   [ROW FORMAT row_format]    
   [STORED AS file_format]
     | STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (...)]  
  ]  -- 指定行分隔符、存储文件格式或采用自定义存储格式
  [LOCATION hdfs_path]  -- 指定表的存储位置
  [TBLPROPERTIES (property_name=property_value, ...)]  --指定表的属性
  [AS select_statement];   --从查询结果创建表
```

{% hint style="info" %}
file\_format包括以下:

* 文本格式 TEXTFILE
* 序列化文件格式 SEQUENCEFILE
* RC文件格式 RCFILE
* ORC文件格式 ORC
* AVRO文件格式 AVRO
* Parquet文件格式 PARQUET
{% endhint %}

### 2.2 内部表

```sql
  CREATE TABLE emp(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

### 2.3 外部表

```sql
  CREATE EXTERNAL TABLE emp_external(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_external';
```

### 2.4 分区表

```sql
  CREATE EXTERNAL TABLE emp_partition(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    PARTITIONED BY (deptno INT)   -- 按照部门编号进行分区
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_partition';
```

### 2.5 分桶表

```sql
  CREATE EXTERNAL TABLE emp_bucket(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2),
    deptno INT)
    CLUSTERED BY(empno) SORTED BY(empno ASC) INTO 4 BUCKETS  --按照员工编号散列到四个 bucket 中
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_bucket';
```

### 2.6 倾斜表

通过指定一个或者多个列经常出现的值（严重偏斜），Hive 会自动将涉及到这些值的数据拆分为单独的文件。在查询时，如果涉及到倾斜值，它就直接从独立文件中获取数据，而不是扫描所有文件，这使得性能得到提升。

```sql
  CREATE EXTERNAL TABLE emp_skewed(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    SKEWED BY (empno) ON (66,88,100)  --指定 empno 的倾斜值 66,88,100
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
    LOCATION '/hive/emp_skewed';   
```

### 2.7 临时表

临时表仅对当前 session 可见，临时表的数据将存储在用户的暂存目录中，并在会话结束后删除。

```sql
  CREATE TEMPORARY TABLE emp_temp(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

### 2.8 CTAS创建表

支持从查询语句的结果创建表：

```sql
CREATE TABLE emp_copy AS SELECT * FROM emp WHERE deptno='20';
```

### 2.9 复制表结构

语法：

```
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name  --创建表表名
   LIKE existing_table_or_view_name  --被复制表的表名
   [LOCATION hdfs_path]; --存储位置
```

示例：

```sql
CREATE TEMPORARY EXTERNAL TABLE  IF NOT EXISTS  emp_co  LIKE emp
```

## 三、修改表

```sql
--重命名表
ALTER TABLE emp_temp RENAME TO new_emp;
--新增列
ALTER TABLE emp_temp ADD COLUMNS (address STRING COMMENT 'home address');
```

### 3.2 修改列

```
ALTER TABLE table_name [PARTITION partition_spec] CHANGE [COLUMN] col_old_name col_new_name column_type
  [COMMENT col_comment] [FIRST|AFTER column_name] [CASCADE|RESTRICT];
```

```sql
-- 修改字段名和类型
ALTER TABLE emp_temp CHANGE empno empno_new INT;
 
-- 修改字段 sal 的名称 并将其放置到 empno 字段后
ALTER TABLE emp_temp CHANGE sal sal_new decimal(7,2)  AFTER ename;

-- 为字段增加注释
ALTER TABLE emp_temp CHANGE mgr mgr_new INT COMMENT 'this is column mgr';
```

## 四、清空表/删除表

### 4.1 清空表

```sql
-- 清空整个表或表指定分区中的数据
TRUNCATE TABLE table_name [PARTITION (partition_column = partition_col_value,  ...)];
```

### 4.2 删除表

```sql
DROP TABLE [IF EXISTS] table_name [PURGE]; 
```

{% hint style="info" %}
* 内部表：不仅会删除表的元数据，同时会删除 HDFS 上的数据；
* 外部表：只会删除表的元数据，不会删除 HDFS 上的数据；
* 删除视图引用的表时，不会给出警告（但视图已经无效了，必须由用户删除或重新创建）。
{% endhint %}

