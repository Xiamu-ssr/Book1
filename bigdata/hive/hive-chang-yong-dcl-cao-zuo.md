# Hive常用DCL操作

DCL（Data Control Language，数据控制语言）是一种用于控制数据库对象的访问权限的语言。常见的DCL命令包括：

1. GRANT：授权用户访问数据库对象。
2. REVOKE：撤销已授权用户的数据库对象访问权限。
3. DENY：拒绝用户对数据库对象的访问权限。
4. AUDIT：对用户对数据库对象的访问进行审计。
5. COMMENT：对数据库对象添加注释或备注信息。

## 一、Grant

### 1. 查询

查询某个用户在某个库上的权限

```sql
SHOW GRANT ON DATABASE database_name TO user_name;
```

查看某个用户在所有库的权限

```
// Some code
```
