# 构建m

创建容器

{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.2 -p 8080:8080 -p 8088:8088 -p 3000:3000 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -it --name=bgm xiamussr/bg-b:1.0 /usr/sbin/init
```
{% endcode %}

安装mysql

```
yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm && \
rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 && \
yum install -y mysql-community-server && \
systemctl start mysqld && \
systemctl enable mysqld && \
systemctl status mysqld
```

进入mysql

```
grep 'temporary password' /var/log/mysqld.log && mysql -u root -p
```

重置密码并设置底策略密码

```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MKLmkl11@@';FLUSH PRIVILEGES;
SET GLOBAL validate_password_policy='LOW';
SET GLOBAL validate_password_length=6;
SET GLOBAL validate_password_mixed_case_count=0;
SET GLOBAL validate_password_number_count=0;
SET GLOBAL validate_password_special_char_count=0;
SHOW VARIABLES LIKE 'validate_password%';
```

安装配置ntp

```
yum install ntp -y && vi /etc/ntp.conf
```

```
#修改
#restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
#为
restrict 172.19.0.0 mask 255.255.255.0 nomodify notrap

#注释
#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst
# 添加如下，使用阿里云服务器时间
server ntp1.aliyun.com iburst
server ntp2.aliyun.com iburst
server ntp3.aliyun.com iburst
server ntp4.aliyun.com iburst
server ntp5.aliyun.com iburst
server ntp6.aliyun.com iburst
server ntp7.aliyun.com iburst

#追加，当该节点丢失网络连接，依然可以采用本地时间作为时间服务器为集群中的其他节点提供时间同步
server 127.127.1.0
fudge 127.127.1.0 stratum 10
```

```
systemctl start ntpd && \
systemctl enable ntpd && \
systemctl status ntpd
```

安装http

```
yum install -y httpd && \
systemctl start httpd && \
systemctl enable httpd && \
systemctl status httpd
```

打包

```
docker commit bgm xiamussr/bg-m:1.0
```
