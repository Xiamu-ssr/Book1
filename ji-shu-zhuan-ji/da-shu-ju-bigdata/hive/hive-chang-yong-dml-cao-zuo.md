# Hive常用DML操作

## 一、加载文件数据到表

### 1.1 语法

```
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] 
INTO TABLE tablename [PARTITION (partcol1=val1, partcol2=val2 ...)]
```

使用建议：

* 不论是本地路径还是 URL 都建议使用完整的
* 加载对象是分区表时建议显示指定分区

### 1.2 示例

新建分区表：

```sql
  CREATE TABLE emp_ptn(
    empno INT,
    ename STRING,
    job STRING,
    mgr INT,
    hiredate TIMESTAMP,
    sal DECIMAL(7,2),
    comm DECIMAL(7,2)
    )
    PARTITIONED BY (deptno INT)   -- 按照部门编号进行分区
    ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

从 HDFS 上加载数据到分区表：

```sql
LOAD DATA  INPATH "hdfs://hadoop001:8020/mydir/emp.txt" OVERWRITE INTO TABLE emp_ptn PARTITION (deptno=20);
```

## 二、查询结果插入到表

### 2.1 语法

```
INSERT OVERWRITE TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...) [IF NOT EXISTS]]   
select_statement1 FROM from_statement;

INSERT INTO TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...)] 
select_statement1 FROM from_statement;
```

可以将 SELECT 语句的查询结果插入多个表（或分区），称为多表插入。语法如下：

```
FROM from_statement
INSERT OVERWRITE TABLE tablename1 
[PARTITION (partcol1=val1, partcol2=val2 ...) [IF NOT EXISTS]] select_statement1
[INSERT OVERWRITE TABLE tablename2 [PARTITION ... [IF NOT EXISTS]] select_statement2]
[INSERT INTO TABLE tablename2 [PARTITION ...] select_statement2] ...;
```

### 2.2 动态插入分区

```
INSERT OVERWRITE TABLE tablename PARTITION (partcol1[=val1], partcol2[=val2] ...) 
select_statement FROM from_statement;

INSERT INTO TABLE tablename PARTITION (partcol1[=val1], partcol2[=val2] ...) 
select_statement FROM from_statement;
```

在向分区表插入数据时候，分区列名是必须的，但是列值是可选的。如果给出了分区列值，我们将其称为静态分区，否则它是动态分区。动态分区列必须在 SELECT 语句的列中最后指定，并且与它们在 PARTITION() 子句中出现的顺序相同。

### 2.3 示例

1. 新建 emp 表，作为查询对象表

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
    
 -- 加载数据到 emp 表中 这里直接从本地加载
load data local inpath "/usr/file/emp.txt" into table emp;
```

​ 完成后 `emp` 表中数据如下：

<figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

2. 为清晰演示，先清空 `emp_ptn` 表中加载的数据：

```sql
TRUNCATE TABLE emp_ptn;
```

3. 静态分区演示：从 `emp` 表中查询部门编号为 20 的员工数据，并插入 `emp_ptn` 表中，语句如下：

```sql
INSERT OVERWRITE TABLE emp_ptn PARTITION (deptno=20) 
SELECT empno,ename,job,mgr,hiredate,sal,comm FROM emp WHERE deptno=20;
```

<figure><img src="../../../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

4. 接着演示动态分区：

```sql
-- 由于我们只有一个分区，且还是动态分区，所以需要关闭严格默认。因为在严格模式下，用户必须至少指定一个静态分区
set hive.exec.dynamic.partition.mode=nonstrict;

-- 动态分区   此时查询语句的最后一列为动态分区列，即 deptno
INSERT OVERWRITE TABLE emp_ptn PARTITION (deptno) 
SELECT empno,ename,job,mgr,hiredate,sal,comm,deptno FROM emp WHERE deptno=30;
```

<figure><img src="../../../.gitbook/assets/image (4) (1).png" alt=""><figcaption></figcaption></figure>

## 三、使用SQL语句插入值

```
INSERT INTO TABLE tablename [PARTITION (partcol1[=val1], partcol2[=val2] ...)] 
VALUES ( value [, value ...] )
```

* 使用时必须为表中的每个列都提供值。不支持只向部分列插入值（可以为缺省值的列提供空值来消除这个弊端）；
* 如果目标表表支持 ACID 及其事务管理器，则插入后自动提交；
* 不支持支持复杂类型 (array, map, struct, union) 的插入。

## 四、更新和删除数据

### 4.1 语法

更新和删除的语法比较简单，和关系型数据库一致。需要注意的是这两个操作都只能在支持 ACID 的表，也就是事务表上才能执行。

```
-- 更新
UPDATE tablename SET column = value [, column = value ...] [WHERE expression]

--删除
DELETE FROM tablename [WHERE expression]
```

## 五、查询结果写出到文件系统

### 5.1 语法

```
INSERT OVERWRITE [LOCAL] DIRECTORY directory1
  [ROW FORMAT row_format] [STORED AS file_format] 
  SELECT ... FROM ...
```

### 5.2 示例

```sql
INSERT OVERWRITE LOCAL DIRECTORY '/usr/file/ouput'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
SELECT * FROM emp_ptn;
```
