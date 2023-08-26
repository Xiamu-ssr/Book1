# Hive简介及核心概念

## 一、简介

Hive 是一个构建在 Hadoop 之上的数据仓库，它可以将结构化的数据文件映射成表，并提供类 SQL 查询功能，用于查询的 SQL 语句会被转化为 MapReduce 作业，然后提交到 Hadoop 上运行。

**特点**：

1. 简单、容易上手 (提供了类似 sql 的查询语言 hql)，使得精通 sql 但是不了解 Java 编程的人也能很好地进行大数据分析；
2. 灵活性高，可以自定义用户函数 (UDF) 和存储格式；
3. 为超大的数据集设计的计算和存储能力，集群扩展容易;
4. 统一的元数据管理，可与 presto／impala／sparksql 等共享数据；
5. 执行延迟高，不适合做数据的实时处理，但适合做海量数据的离线处理。

## 二、Hive的体系架构

### 2.2 Metastore

在 Hive 中，表名、表结构、字段名、字段类型、表的分隔符等统一被称为元数据。所有的元数据默认存储在 Hive 内置的 derby 数据库中，但由于 derby 只能有一个实例，也就是说不能有多个命令行客户端同时访问，所以在实际生产环境中，通常使用 MySQL 代替 derby。

Hive 进行的是统一的元数据管理，就是说你在 Hive 上创建了一张表，然后在 presto／impala／sparksql 中都是可以直接使用的，它们会从 Metastore 中获取统一的元数据信息，同样的你在 presto／impala／sparksql 中创建一张表，在 Hive 中也可以直接使用。

### 2.3 HQL的执行流程

Hive 在执行一条 HQL 的时候，会经过以下步骤：

1. 语法解析：Antlr 定义 SQL 的语法规则，完成 SQL 词法，语法解析，将 SQL 转化为抽象 语法树 AST Tree；
2. 语义解析：遍历 AST Tree，抽象出查询的基本组成单元 QueryBlock；
3. 生成逻辑执行计划：遍历 QueryBlock，翻译为执行操作树 OperatorTree；
4. 优化逻辑执行计划：逻辑层优化器进行 OperatorTree 变换，合并不必要的 ReduceSinkOperator，减少 shuffle 数据量；
5. 生成物理执行计划：遍历 OperatorTree，翻译为 MapReduce 任务；
6. 优化物理执行计划：物理层优化器进行 MapReduce 任务的变换，生成最终的执行计划。

## 三、数据类型

### 3.1 基本数据类型

Hive 表中的列支持以下基本数据类型：

<table><thead><tr><th width="337">大类</th><th>类型</th></tr></thead><tbody><tr><td><strong>Integers（整型）</strong></td><td>TINYINT—1 字节的有符号整数<br>SMALLINT—2 字节的有符号整数<br>INT—4 字节的有符号整数<br>BIGINT—8 字节的有符号整数</td></tr><tr><td><strong>Boolean（布尔型）</strong></td><td>BOOLEAN—TRUE/FALSE</td></tr><tr><td><strong>Floating point numbers（浮点型）</strong></td><td>FLOAT— 单精度浮点型<br>DOUBLE—双精度浮点型</td></tr><tr><td><strong>Fixed point numbers（定点数）</strong></td><td>DECIMAL—用户自定义精度定点数，比如 DECIMAL(7,2)</td></tr><tr><td><strong>String types（字符串）</strong></td><td>STRING—指定字符集的字符序列<br>VARCHAR—具有最大长度限制的字符序列<br>CHAR—固定长度的字符序列</td></tr><tr><td><strong>Date and time types（日期时间类型）</strong></td><td>TIMESTAMP — 时间戳<br>TIMESTAMP WITH LOCAL TIME ZONE — 时间戳，纳秒精度<br>DATE—日期类型</td></tr><tr><td><strong>Binary types（二进制类型）</strong></td><td>BINARY—字节序列</td></tr></tbody></table>

{% hint style="info" %}
TIMESTAMP 和 TIMESTAMP WITH LOCAL TIME ZONE 的区别如下：

* **TIMESTAMP WITH LOCAL TIME ZONE**：用户提交时间给数据库时，会被转换成数据库所在的时区来保存。查询时则按照查询客户端的不同，转换为查询客户端所在时区的时间。
* **TIMESTAMP** ：提交什么时间就保存什么时间，查询时也不做任何转换。
{% endhint %}

### 3.3 复杂类型

<table><thead><tr><th width="124.33333333333331">类型</th><th>描述</th><th>示例</th></tr></thead><tbody><tr><td><strong>STRUCT</strong></td><td>类似于对象，是字段的集合，字段的类型可以不同，可以使用 <code>名称.字段名</code> 方式进行访问</td><td>STRUCT ('xiaoming', 12 , '2018-12-12')</td></tr><tr><td><strong>MAP</strong></td><td>键值对的集合，可以使用 <code>名称[key]</code> 的方式访问对应的值</td><td>map('a', 1, 'b', 2)</td></tr><tr><td><strong>ARRAY</strong></td><td>数组是一组具有相同类型和名称的变量的集合，可以使用 <code>名称[index]</code> 访问对应的值</td><td>ARRAY('a', 'b', 'c', 'd')</td></tr></tbody></table>

### 3.4 示例

```sql
CREATE TABLE students(
  name      STRING,   -- 姓名
  age       INT,      -- 年龄
  subject   ARRAY<STRING>,   --学科
  score     MAP<STRING,FLOAT>,  --各个学科考试成绩
  address   STRUCT<houseNumber:int, street:STRING, city:STRING, province：STRING>  --家庭居住地址
) ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```
