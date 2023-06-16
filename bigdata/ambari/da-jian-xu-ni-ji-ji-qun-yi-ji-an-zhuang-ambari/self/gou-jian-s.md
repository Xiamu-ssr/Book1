# 构建s

```
yum install chrony -y && vi /etc/chrony.conf
```

```
# 找到 server 部分，添加以下行
# Use the main server as the time source
server 172.19.0.2 iburst
```
