# 进阶-函数

## 时间函数

<details>

<summary>from_unixtime</summary>

把Unix时间戳（以秒为单位）转换成日期和时间的字符串。有两个参数，第一个参数是Unix时间戳，第二个参数是日期和时间的格式，如果省略第二个参数，那么默认的格式是yyyy-MM-dd HH:mm:ss

```sql
SELECT from_unixtime(1640995199); -- 返回'2021-12-31 23:59:59'
SELECT from_unixtime(1640995199, 'yyyy-MM-dd'); -- 返回'2021-12-31'
```

</details>

<details>

<summary>unix_timestamp</summary>

把日期和时间的字符串转换成Unix时间戳（以秒为单位）。它有两个参数，第一个参数是日期和时间的字符串，第二个参数是日期和时间的格式，如果省略第二个参数，那么默认的格式是yyyy-MM-dd HH:mm:ss。

```sql
SELECT unix_timestamp('2021-12-31 23:59:59'); -- 返回1640995199
SELECT unix_timestamp('2021-12-31', 'yyyy-MM-dd'); -- 返回1640956800
```

</details>

<details>

<summary>collect_list</summary>

好的，我可以举一个具体的例子来描述map和collect函数。假设我们有一个表叫student，它有三列：id, name, score，如下所示：

```
id	name	score
1	Tom	80
2	Lily	90
3	Jack	85
1	Tom	75
2	Lily	95
3	Jack	80
```

如果我们想要把每个学生的所有成绩收集到一个数组中，我们可以用collect函数，像这样：

select id, name, collect\_list(score) as scores from student group by id, name;

这样就会得到下面的结果：

```
id	name	scores
1	Tom	[80, 75]
2	Lily	[90, 95]
3	Jack	[85, 80]
```

</details>

<details>

<summary>map</summary>

好的，我可以举一个具体的例子来描述map和collect函数。假设我们有一个表叫student，它有三列：id, name, score，如下所示：

```
id	name	score
1	Tom	80
2	Lily	90
3	Jack	85
1	Tom	75
2	Lily	95
3	Jack	80
```

select id, map(name, score\_array) as name\_score\_map from ( select id, name, array(score) as score\_array from student ) t;

这样就会得到下面的结果：

```
id	name_score_map
1	{‘Tom’: [80]}
1	{‘Tom’: [75]}
2	{‘Lily’: [90]}
2	{‘Lily’: [95]}
3	{‘Jack’: [85]}
3	{‘Jack’: [80]}
```

</details>

<details>

<summary>datediff</summary>

计算date类型变量之差

`datediff('1920-01-01', date)` 函数用于计算date日期和'1920-01-01'日期之间相差的天数。这个函数返回一个整数值。

</details>

<details>

<summary>pmod</summary>

取余计算

`pmod(45,7)`计算45对7取余，返回3

</details>

