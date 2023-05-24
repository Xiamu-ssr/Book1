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

```sh
sudo yum update && sudo yum upgrade #先给新系统更新一下新技能
sudo yum localinstall https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm #添加mysql到yum的安装列表中
sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 #添加对mysql安装的密钥
sudo yum install mysql-community-server.x86_64 #安装mysqljava-1.8.0-openjdk.x86_64

sudo yum install java-1.8.0-openjdk.x86_64 java-1.8.0-openjdk-headless.x86_64 #安装JDK8
```
