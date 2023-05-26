---
description: '8'
---

# MySQL

## 免输密码登录

### 第一种

修改`/etc/my.cnf`，加上`skip-grant-tables`，重启服务

但是这个会和在my.cnf中指定port冲突，使得指定port无效。

### 第二种
