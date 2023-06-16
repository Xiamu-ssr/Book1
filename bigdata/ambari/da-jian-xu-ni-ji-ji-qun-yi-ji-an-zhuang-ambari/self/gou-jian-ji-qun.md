# 构建集群

创建虚拟网络

```
docker network create bigdata --subnet=172.19.0.0/16 --gateway=172.19.0.1 ; `
docker network list
```

创建主节点

{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.2 -p 8080:8080 -p 8088:8088 -p 3000:3000 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgm xiamussr/bg-m:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}

创建3从节点

{% tabs %}
{% tab title="1" %}
{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.3 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs1 xiamussr/bg-s:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}

{% tab title="2" %}
{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.4 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs2 xiamussr/bg-s:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}

{% tab title="3" %}
{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.5 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs3 xiamussr/bg-s:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}
{% endtabs %}

导入Shell脚本文件夹和三压缩包

{% file src="../../../../.gitbook/assets/Shell.zip" %}

```
docker cp .\Shell\ bgm:/root; `
docker exec bgm mkdir /root/Downloads; `
docker cp .\ambari-2.7.4.0-centos7.tar.gz bgm:/root/Downloads/; `
docker cp .\HDP-3.1.4.0-centos7-rpm.tar.gz bgm:/root/Downloads/; `
docker cp .\HDP-UTILS-1.1.0.22-centos7.tar.gz bgm:/root/Downloads/; `
docker exec -it bgm /bin/bash
```

修改config.sh和/etc/hosts后，配置免密

```
cd /root/Shell && \
bash scp_to_all.sh /etc/hosts /etc && \
bash scp_to_all.sh /root/Shell /root && \
bash ssh_all_to_all.sh
```

解压三安装包

```
mkdir /var/www/html/ambari && \
mkdir /var/www/html/hdp && \
mkdir /var/www/html/hdp-utils && \
tar -zxf /root/Downloads/ambari-2.7.4.0-centos7.tar.gz -C /var/www/html/ambari && \
tar -zxf /root/Downloads/HDP-3.1.4.0-centos7-rpm.tar.gz -C /var/www/html/hdp && \
tar -zxf /root/Downloads/HDP-UTILS-1.1.0.22-centos7.tar.gz -C /var/www/html/hdp-utils/ && \
find /var/www/html -maxdepth 2
```

配置repo

```
echo "[ambari]
name=ambari
baseurl=http://172.19.0.2/ambari/ambari/centos7/2.7.4.0-118
gpgcheck=0" | sudo tee /etc/yum.repos.d/ambari.repo && \
echo "[HDP]
name=HDP
baseurl=http://172.19.0.2/hdp/HDP/centos7/3.1.4.0-315
gpgcheck=0
[HDP-UTILS]
name=HDP_UTILS
baseurl=http://172.19.0.2/hdp-utils/HDP-UTILS/centos7/1.1.0.22/
gpgcheck=0" | sudo tee /etc/yum.repos.d/hdp.repo && \
cat /etc/yum.repos.d/ambari.repo && \
echo -e "\n" && \
cat /etc/yum.repos.d/hdp.repo && \
yum clean all && \
yum makecache && \
yum repolist && \
bash /root/Shell/scp_to_all.sh /etc/yum.repos.d/ambari.repo /etc/yum.repos.d/ && \
bash /root/Shell/scp_to_all.sh /etc/yum.repos.d/hdp.repo /etc/yum.repos.d/
```

安装ambari-server

```
yum install -y ambari-server && mysql -u root -p
```

配置数据库

```
SET GLOBAL validate_password_policy='LOW';
SET GLOBAL validate_password_length=6;
SET GLOBAL validate_password_mixed_case_count=0;
SET GLOBAL validate_password_number_count=0;
SET GLOBAL validate_password_special_char_count=0;
SHOW VARIABLES LIKE 'validate_password%';
CREATE USER 'ambari'@'%' IDENTIFIED BY 'bigdata';
create database ambari;
grant all on ambari.* to ambari@'%';
use ambari;
source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql;
show tables;
CREATE DATABASE hive;
CREATE USER 'hive'@'%' IDENTIFIED BY 'hive%123';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%';
FLUSH PRIVILEGES;
```

安装jdbc

```
cd /root/Downloads && \
wget https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-j-8.0.33-1.el7.noarch.rpm && \
rpm -qpl mysql-connector-j-8.0.33-1.el7.noarch.rpm && \
rpm -ivh mysql-connector-j-8.0.33-1.el7.noarch.rpm && \
rpm -qa | grep mysql-connector-j
```

```
ambari-server setup --jdbc-db=mysql --jdbc-driver=/usr/share/java/mysql-connector-java.jar && \
ambari-server setup && \
ambari-server start
```
