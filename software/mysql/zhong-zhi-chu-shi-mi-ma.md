# 重置初始密码

因为初始密码是加密，最多也只能看到加密后的密码，所以没有必要看。

1. 修改`/etc/my.cnf`，加上`skip-grant-tables`，跳过密码验证，重启服务，`mysql -u root`直接进入mysql命令行。
2. 输入`UPDATE mysql.user SET authentication_string=null WHERE User='root';`设置空密码，`FLUSH PRIVILEGES;`刷新权限，退出mysql命令行。
3. 修改`/etc/my.cnf`，注释`skip-grant-tables`，重启服务，`mysql -u root`再次登录。
4. 输入`ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'MKLmkl11@@';`设置一个复杂的密码
5. 然后将密码策略等级设置为低级`SET GLOBAL validate_password.policy=LOW;`
6. 再次输入`ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY '123456';`设置一个简单的密码，`FLUSH PRIVILEGES;`刷新权限，退出

如果遇到密码策略为LOW，但依旧密码安全性过不了，可以查看更多信息`SHOW VARIABLES LIKE 'validate_password%';`然后手动修改。

{% hint style="info" %}
如果使用5.7老版本，用以下方法
{% endhint %}

`sudo grep 'temporary password' /var/log/mysqld.log`直接查看mysql的临时密码，然后`mysql -u root -p` 登录。

输入`ALTER USER 'root'@'localhost' IDENTIFIED BY 'MKLmkl11@@';`修改。`FLUSH PRIVILEGES;`刷新权限，退出

