# +Docker从已有镜像简易部署

### 1. 拉取镜像

```sh
docker pull xiamussr/bigdata-slave:1.0
docker pull xiamussr/bigdata-master:1.0
```

### 2. 创建虚拟网络

```sh
docker network create bigdata --subnet=172.19.0.0/16 --gateway=172.19.0.1
docker network list #查看所有网络
docker network inspect bigdata #查看bigdata网络详细信息
```

### 3. 创建容器

```
docker run --network bigdata --ip 172.19.0.2 -p 8080:8080 \
 --name bg-c79-0 -it --cpus=6 -m 16G --privileged=true \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock \
   --stop-signal=RTMIN+3 \
   xiamussr/bigdata-master:1.0 /usr/sbin/init
```

```sh
docker run --network bigdata --ip 172.19.0.3 --name bg-c79-1 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.4 --name bg-c79-2 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.5 --name bg-c79-3 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.6 --name bg-c79-4 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
```

### 4. 集群通信

写好/etc/hosts，发送给每个slave，参考以下脚本\[0]

{% content-ref url="../../../../linux/linux/jiao-ben.md" %}
[jiao-ben.md](../../../../linux/linux/jiao-ben.md)
{% endcontent-ref %}

配置互相免密，参考以下脚本\[1]

{% content-ref url="../../../../linux/linux/jiao-ben.md" %}
[jiao-ben.md](../../../../linux/linux/jiao-ben.md)
{% endcontent-ref %}

### 5. 解压ambari安装包

```sh
# 这里的-C是指定解压目录
tar -zxf ambari-2.7.4.0-centos7.tar.gz -C /var/www/html/ambari 
tar -zxf HDP-3.1.4.0-centos7-rpm.tar.gz -C /var/www/html/hdp
tar -zxf HDP-UTILS-1.1.0.22-centos7.tar.gz -C /var/www/html/hdp-utils/
```

### 6.加入yum并安装

```sh
# yum创建缓存
yum clean all
yum makecache

# 通过yum repolist命令验证即可
yum repolist
#安装
yum install -y ambari-server
```

### 7. 配置ambari server

```sh
#进入mysql给ambari数据库载入Ambari-DDL-MySQL-CREATE.sql
mysql -u root -p
>use ambari;
>source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql;
>SHOW TABLES;
>quit;

ambari-server setup --jdbc-db=mysql --jdbc-driver=/usr/share/java/mysql-connector-java.jar
#在配置一遍刚才配置的之外的
ambari-server setup
#启动
ambari-server start
```

后面的过程就把赘述了。

