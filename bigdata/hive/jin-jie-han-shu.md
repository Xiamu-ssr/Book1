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
