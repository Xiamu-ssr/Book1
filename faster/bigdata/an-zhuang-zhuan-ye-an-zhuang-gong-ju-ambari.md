# 安装专业安装工具Ambari

这应该是免费版的ambari，需要自己从源码构建，我尝试过ubuntu16.04和centos7，mvn构建不出来，而且过程很长。

{% embed url="https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.7.7" %}

看到网上很多教程包括cloudera自己家的教程，都是添加repo然后使用包管理器直接安装，比如下面这个。然后我发现，资源访问需要付费订阅？去查了一下，在21年的时候就停止免费了，但是很多教程依旧停留在免费的时代，所以一直导致安装过程停滞不前。

{% embed url="https://docs.cloudera.com/HDPDocuments/Ambari-2.5.0.3/bk_ambari-installation/content/ambari_repositories.html" %}

不过这并不难办，互联网上肯定有大量备份。比如我这份教程是按照下面这份教程，然后记录过程的。

{% embed url="https://blog.csdn.net/AnameJL/article/details/122962868" %}

## 1.环境及软件准备

| OS        | CentOS 7.9 in VMware |
| --------- | -------------------- |
| Ambari    | 2.7.4.0              |
| HDP       | 3.1.4.0              |
| HDP-UTILS | 1.1.0.22             |
| Java      | JDK8                 |
| SQL       | Mysql 5.7+           |

Ambari、HDP、HDP-UTILS安装包下载链接如下

{% embed url="https://pan.baidu.com/s/18uH3jvciTj0mFNbHlZiugQ" %}
**提取码：3rwq**
{% endembed %}

## 2.准备工作

### 2.1关闭防火墙

```sh
sudo systemctl status firewalld # 通过此命令查看防火墙状态
sudo systemctl stop firewalld # 关闭防火墙
sudo systemctl disable firewalld # 关闭防火墙开机自启
```

### 2.2安装JDK

<pre class="language-sh"><code class="lang-sh"><strong>sudo yum install java-1.8.0-openjdk.x86_64 java-1.8.0-openjdk-headless.x86_64
</strong>
readlink -f /usr/bin/java #查看java安装位置

sudo vim /etc/profile
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.372.b07-1.el7_9.x86_64/jre
export PATH=$PATH:$JAVA_HOME/bin

</code></pre>

### 2.3安装MySQL

```sh
sudo yum localinstall https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm #添加mysql到yum的安装列表中
sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 #添加对mysql安装的密钥
sudo yum install mysql-community-server.x86_64 #安装mysqljava-1.8.0-openjdk.x86_64
```

重置初始密码和免输密码登录

{% content-ref url="../../debug/mysql/" %}
[mysql](../../debug/mysql/)
{% endcontent-ref %}

修改`/etc/my.cnf`添加以下配置

```
[mysqld]
port=3306
bind-address=0.0.0.0
```

```sh
systemctl restart mysqld #开启服务
netstat -nltp | grep 3306 # 查看mysql默认的3306端口号是否存在
systemctl enable mysqld # 将mysql服务加入到开机自启
```

### 2.4关闭SELinux

```sh
# 临时性关闭（立即生效，但是重启服务器后失效）
setenforce 0 #设置selinux为permissive模式（即关闭）
setenforce 1 #设置selinux为enforcing模式（即开启）
# 永久性关闭（这样需要重启服务器后生效）
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
```

然后reboot重启，`sestatus`查看SELinux状态

### 2.5克隆额外两台服务器

使用VMware克隆功能，选择完全克隆。

