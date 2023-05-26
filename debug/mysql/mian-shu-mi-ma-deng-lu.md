# 免输密码登录

## 第一种

修改`/etc/my.cnf`，加上`skip-grant-tables`，重启服务

但是这个会和在my.cnf中指定port冲突，使得指定port无效。

## 第二种

修改`/etc/my.cnf`，添加以下内容

```sh
[client]
user=root
password=password
```

重启服务

如果觉得这太容易泄露了，可以`chmod 400 my.cnf`只让自己可读
