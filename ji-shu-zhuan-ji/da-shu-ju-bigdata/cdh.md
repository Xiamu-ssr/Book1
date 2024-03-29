---
description: 因为Ambari的Tez无法解决，退坑了。
---

# CDH

内容参考以下博客

{% embed url="https://www.jianshu.com/p/adfa7cfbdfb3" %}
参考教程
{% endembed %}

CDH及其他资源下载

{% embed url="https://pan.baidu.com/s/1r_-sqW5DqlXrTb9fdwfLag" %}
提取码 : u07l
{% endembed %}

## 一、前置任务

创建docker自定义网络

```sh
docker network create --subnet=172.10.0.0/16 CDH
```

下载上述资源

在下载后CDH文件夹中，Dockerfile同级目录执行以下命令来创建基础系统镜像

```sh
docker build -t centos7-cdh .
```

## 二、构建主节点

### 2.1 初始化环境

启动容器

<pre class="language-bash"><code class="lang-bash">docker run -d `
<strong>--add-host cm.hadoop:172.10.0.2 `
</strong>--net CDH `
--ip 172.10.0.2 `
-h cm.hadoop `
-p 10022:22 `
-p 7180:7180 `
--name cm.hadoop `
--privileged=true `
-v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock `
--stop-signal=RTMIN+3 `
centos7-cdh `
/usr/sbin/init
</code></pre>

拷贝hadoop\_CDH资源文件夹到主节点

```sh
docker cp hadoop_CDH cm.hadoop:/root/hadoop_CDH
```

进入主节点

```sh
docker exec -it cm.hadoop /bin/bash
```

设置root密码

```bash
passwd
1009
1009
```

安装常用证书，然后换清华源,升级并安装基础软件包

{% embed url="https://mirrors.tuna.tsinghua.edu.cn/help/centos/" %}
清华镜像
{% endembed %}

```bash
yum install -y ca-certificates 
#换源
yum update -y && yum upgrade -y
yum install -y kde-l10n-Chinese telnet reinstall glibc-common vim wget ntp net-tools ca-certificates sshpass pssh
yum clean all
```

### 2.2 配置中文环境

```bash
(
cat <<EOF
export LC_ALL=zh_CN.utf8
export LANG=zh_CN.utf8
export LANGUAGE=zh_CN.utf8
EOF
) >> ~/.bashrc \
&& localedef -c -f UTF-8 -i zh_CN zh_CN.utf8 \
&& source ~/.bashrc \
&& echo $LANG
```

### 2.3 设置时间同步

```
vim /etc/ntp.conf
```

更改为以下四个时钟服务器

```
server 0.cn.pool.ntp.org
server 1.cn.pool.ntp.org
server 2.cn.pool.ntp.org
server 3.cn.pool.ntp.org
```

调整时区

```bash
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

启动ntp服务

```bash
systemctl start ntpd && \
systemctl enable ntpd && \
ntpdate -u 0.cn.pool.ntp.org && \
hwclock --systohc && \
date
```

### 2.4 搭建本地yum源

```bash
yum -y install httpd createrepo \
&& systemctl start httpd \
&& systemctl enable httpd \
&& cd /root/hadoop_CDH/cloudera-repos/ && createrepo . \
&& mv /root/hadoop_CDH/cloudera-repos /var/www/html/ \
&& yum clean all \
&& ll /var/www/html/cloudera-repos
```

### 2.5安装jdk

```bash
cd /var/www/html/cloudera-repos/

rpm -ivh oracle-j2sdk1.8-1.8.0update181-1.x86_64.rpm
```

### 2.6安装配置MySQL数据库

```
cd /root/hadoop_CDH/mysql/

tar -xvf mysql-5.7.27-1.el7.x86_64.rpm-bundle.tar \
&& yum install -y libaio numactl \
&& rpm -ivh mysql-community-common-5.7.27-1.el7.x86_64.rpm \
&& rpm -ivh mysql-community-libs-5.7.27-1.el7.x86_64.rpm \
&& rpm -ivh mysql-community-client-5.7.27-1.el7.x86_64.rpm \
&& rpm -ivh mysql-community-server-5.7.27-1.el7.x86_64.rpm \
&& rpm -ivh mysql-community-libs-compat-5.7.27-1.el7.x86_64.rpm \
&& echo character-set-server=utf8 >> /etc/my.cnf \
&& rm -rf /root/hadoop_CDH/mysql/ \
&& yum clean all \
&& rpm -qa |grep mysql
```

### 2.7数据库授权

```bash
(
cat <<EOF
set password for root@localhost = password('123456Aa.');
grant all privileges on *.* to 'root'@'%' identified by '123456Aa.';
flush privileges;
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE hue DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE metastore DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE sentry DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE nav DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE navms DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE DATABASE oozie DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON scm.* TO 'scm'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON amon.* TO 'amon'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON rman.* TO 'rman'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON hue.* TO 'hue'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON metastore.* TO 'hive'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON sentry.* TO 'sentry'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON nav.* TO 'nav'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON navms.* TO 'navms'@'%' IDENTIFIED BY '123456Aa.';
GRANT ALL ON oozie.* TO 'oozie'@'%' IDENTIFIED BY '123456Aa.';
SHOW DATABASES;
EOF
) >> /root/c.sql
```

获取MySQL初始密码

```bash
systemctl start mysqld && grep password /var/log/mysqld.log | sed 's/.*\(............\)$/\1/'
```

使用密码登录进入mysql

```bash
mysql -u root –p
```

登陆后执行

```bash
source /root/c.sql
```

### 2.8配置mysql jdbc驱动

```bash
mkdir -p /usr/share/java/ \
&& cd /root/hadoop_CDH/mysql-jdbc/;tar -zxvf mysql-connector-java-5.1.48.tar.gz \
&& cp  /root/hadoop_CDH/mysql-jdbc/mysql-connector-java-5.1.48/mysql-connector-java-5.1.48-bin.jar /usr/share/java/mysql-connector-java.jar \
&& rm -rf /root/hadoop_CDH/mysql-jdbc/ \
&& ls /usr/share/java/
```

### 2.9安装Cloudera Manager

```bash
(
cat <<EOF
[cloudera-manager]
name=Cloudera Manager 6.3.0
baseurl=http://172.10.0.2/cloudera-repos/
gpgcheck=0
enabled=1
EOF
) >> /etc/yum.repos.d/cloudera-manager.repo \
&& yum clean all \
&& yum makecache \
&& yum install -y cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server \
&& yum clean all \
&& rpm -qa | grep cloudera-manager
```

### 2.10配置parcel库

```bash
cd /opt/cloudera/parcel-repo/;mv /root/hadoop_CDH/parcel/* ./ \
&& sha1sum CDH-6.3.2-1.cdh6.3.2.p0.1605554-el7.parcel | awk '{ print $1 }' > CDH-6.3.2-1.cdh6.3.2.p0.1605554-el7.parcel.sha \
&& rm -rf /root/hadoop_CDH/parcel/ \
&& chown -R cloudera-scm:cloudera-scm /opt/cloudera/parcel-repo/* \
&& ll /opt/cloudera/parcel-repo/
```

### 2.11初始化scm库

```bash
/opt/cloudera/cm/schema/scm_prepare_database.sh mysql scm scm 123456Aa.
```

### 2.12启动cloudera-server服务

```bash
systemctl start cloudera-scm-server \
&& sleep 2 \
&& tail -f /var/log/cloudera-scm-server/cloudera-scm-server.log | grep "INFO WebServerImpl:com.cloudera.server.cmf.WebServerImpl: Started Jetty server"
```

## 三、配置从节点

以下为worker容器的准备方式，若为多个时，重复执行以下步骤，创建多个worker节点。

### 3.1创建多个worker容器

```bash
docker run -d `
--add-host cm.hadoop:172.10.0.2 `
--add-host cdh01.hadoop:172.10.0.3 `
--net CDH `
--ip 172.10.0.3 `
-h cdh01.hadoop `
-p 20022:22 `
--name cdh01.hadoop `
--privileged=true `
-v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock `
--stop-signal=RTMIN+3 `
centos7-cdh `
/usr/sbin/init 
```

以此类推

{% tabs %}
{% tab title="2" %}
```bash
docker run -d `
--add-host cm.hadoop:172.10.0.2 `
--add-host cdh02.hadoop:172.10.0.4 `
--net CDH `
--ip 172.10.0.4 `
-h cdh02.hadoop `
-p 30022:22 `
--name cdh02.hadoop `
--privileged=true `
-v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock `
--stop-signal=RTMIN+3 `
centos7-cdh `
/usr/sbin/init 
```
{% endtab %}

{% tab title="3" %}
```
docker run -d `
--add-host cm.hadoop:172.10.0.2 `
--add-host cdh03.hadoop:172.10.0.5 `
--net CDH `
--ip 172.10.0.5 `
-h cdh03.hadoop `
-p 40022:22 `
--name cdh03.hadoop `
--privileged=true `
-v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock `
--stop-signal=RTMIN+3 `
centos7-cdh `
/usr/sbin/init 
```
{% endtab %}

{% tab title="4" %}
```
docker run -d `
--add-host cm.hadoop:172.10.0.2 `
--add-host cdh04.hadoop:172.10.0.6 `
--net CDH `
--ip 172.10.0.6 `
-h cdh04.hadoop `
-p 50022:22 `
--name cdh04.hadoop `
--privileged=true `
-v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock `
--stop-signal=RTMIN+3 `
centos7-cdh `
/usr/sbin/init 
```
{% endtab %}
{% endtabs %}

### 3.2配置免密

进入所有从节点，配置root密码和主节点一样。

进入主节点，/etc/hosts添加如下

```
172.10.0.2      cm.hadoop cm
172.10.0.3      cdh01.hadoop cdh01
172.10.0.4      cdh02.hadoop cdh02
172.10.0.5      cdh03.hadoop cdh03
```

按照下面指示创建脚本文件

{% content-ref url="../linux/linux/jiao-ben.md" %}
[jiao-ben.md](../linux/linux/jiao-ben.md)
{% endcontent-ref %}

修改config.sh后把/etc/hosts和/root/Shell发送给所有节点一份

```bash
bash scp_to_all.sh /etc/hosts /etc/
bash scp_to_all.sh /root/Shell /root
```

配置主节点到所有节点的免密

```bash
bash ssh_one_to_all.sh
```

创建host.txt文件，写入从节点名称

```
cdh01.hadoop
cdh02.hadoop
cdh03.hadoop
```

### 3.3装基本工具

给所有从节点安装常用证书

```bash
pssh -h host.txt yum install -y ca-certificates
```

创建tmp.sh，写入以下内容

```
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org/centos|baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo
```

让从节点都执行这个本地(主节点)脚本，来更新清华源

```bash
pssh -h host.txt -I < tmp.sh 
pssh -h host.txt -t 360 yum makecache -y
pssh -h host.txt -t 360 yum update -y
pssh -h host.txt -t 360 yum upgrade -y
```

安装基础软件包

```bash
pssh -h host.txt -t 360 yum -y install kde-l10n-Chinese telnet reinstall glibc-common vim wget ntp net-tools
pssh -h host.txt -t 360 yum -y clean all
```

### 3.4配置中文环境变量

将以下内容写入tmp.sh

```
(
cat <<EOF
export LC_ALL=zh_CN.utf8
export LANG=zh_CN.utf8
export LANGUAGE=zh_CN.utf8
EOF
) >> ~/.bashrc \
&& localedef -c -f UTF-8 -i zh_CN zh_CN.utf8 \
&& source ~/.bashrc \
&& echo $LANG
```

```bash
pssh -h host.txt -I < tmp.sh
```

### 3.5配置NTP时间同步服务

更改四个时钟服务器

```bash
bash scp_to_all.sh /etc/ntp.conf /etc
```

调整时区

```bash
pssh -h host.txt cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

启动ntp服务，将以下写入sh

```bash
systemctl start ntpd && \
systemctl enable ntpd && \
ntpdate -u 0.cn.pool.ntp.org && \
hwclock --systohc && \
date
```

```bash
pssh -h host.txt -I < tmp.sh
```

{% hint style="info" %}
这里出现Failure并不代表从节点调整时间失败，可以手动检查一下
{% endhint %}

### 3.6配置MySQL JDBC

写入sh后pssh

```
mkdir -p /usr/share/java/ \
&& wget -O /usr/share/java/mysql-connector-java-5.1.48.tar.gz \
https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.48.tar.gz \
&& cd /usr/share/java/;tar -zxvf mysql-connector-java-5.1.48.tar.gz \
&& cp /usr/share/java/mysql-connector-java-5.1.48/mysql-connector-java-5.1.48-bin.jar /usr/share/java/mysql-connector-java.jar \
&& rm -rf mysql-connector-java-5.1.48 mysql-connector-java-5.1.48.tar.gz \
&& ls /usr/share/java/
```

## 四、CM管理平台创建CDH集群

### 4.1登陆CM管理平台

[http://IP:7180](https://links.jianshu.com/go?to=http%3A%2F%2FIP%3A7180%2Fcmf%2Flogin)

账号密码：admin/admin

### 4.2欢迎页

同意协议并选择免费套餐

### 4.3集群安装

{% tabs %}
{% tab title="1" %}
填集群名字
{% endtab %}

{% tab title="2" %}
主机名称填 172.10.0.\[2-5]，端口默认22，然后点击搜索，继续


{% endtab %}

{% tab title="3" %}
<figure><img src="../../.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>

自定义存储库：[http://172.10.0.2/cloudera-repos](https://links.jianshu.com/go?to=http%3A%2F%2F172.10.0.2%2Fcloudera-repos)
{% endtab %}

{% tab title="4" %}
<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

Jdk安装
{% endtab %}

{% tab title="5" %}
<figure><img src="../../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

用户为root，密码为容器root用户的登录密码。
{% endtab %}

{% tab title="6" %}
等待安装agent服务。
{% endtab %}

{% tab title="7" %}
等待Parcel 下载并安装。
{% endtab %}

{% tab title="8" %}
检查集群，如果出现warn或error，根据提示修复或完善。
{% endtab %}
{% endtabs %}

### 4.4集群设置

{% tabs %}
{% tab title="1" %}
<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

自定义服务
{% endtab %}

{% tab title="2" %}
<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

各个组件具体安装在哪，仅供参考
{% endtab %}

{% tab title="3" %}
<figure><img src="../../.gitbook/assets/image (2) (2).png" alt=""><figcaption></figcaption></figure>

数据库选择。数据库，用户名，密码，在2.7的脚本里看。
{% endtab %}

{% tab title="4" %}
Datanode-> /dfs/datanode&#x20;

Namenode-> /dfs/namenode&#x20;

HDFS检查点-> /dfs/checkpoint&#x20;

NodeManager 本地目录-> /dfs/nodemanager
{% endtab %}

{% tab title="5" %}
首次运行，并检查所有服务
{% endtab %}
{% endtabs %}
