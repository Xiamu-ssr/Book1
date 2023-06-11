# Page 1

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
