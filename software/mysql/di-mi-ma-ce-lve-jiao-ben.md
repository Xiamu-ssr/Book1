# 低密码策略脚本

使用root用户登录后source此sql脚本

```sql
SET GLOBAL validate_password.policy='LOW';
SHOW VARIABLES LIKE 'validate_password%';
```

如果不奏效，用下面这个。

```sql
SET GLOBAL validate_password.policy='LOW';
SET GLOBAL validate_password.length=6;
SET GLOBAL validate_password.mixed_case_count=0;
SET GLOBAL validate_password.number_count=0;
SET GLOBAL validate_password.special_char_count=0;
SHOW VARIABLES LIKE 'validate_password%';
```

{% hint style="info" %}
mysql 5.7用这个
{% endhint %}

```sql
SET GLOBAL validate_password_policy='LOW';
SET GLOBAL validate_password_length=6;
SET GLOBAL validate_password_mixed_case_count=0;
SET GLOBAL validate_password_number_count=0;
SET GLOBAL validate_password_special_char_count=0;
SHOW VARIABLES LIKE 'validate_password%';
```
