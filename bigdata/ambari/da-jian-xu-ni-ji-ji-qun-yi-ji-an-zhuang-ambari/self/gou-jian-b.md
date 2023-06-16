# 构建b

拉取centos7镜像，创建并进入容器

{% code overflow="wrap" %}
```
docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -it --name=bginit centos:centos7 /usr/sbin/init
```
{% endcode %}

设置密码1009

```
passwd
```

换源

```
yum install -y ca-certificates && \
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org/centos|baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo && \
yum makecache -y
```

安装软件包

```
yum update -y && yum install epel-release -y && yum upgrade -y && \
yum install -y htop sudo net-tools git wget curl initscripts openssh openssh-server cronie sshpass pssh
```

安装JDK

```
yum install -y java-1.8.0-openjdk.x86_64 java-1.8.0-openjdk-devel.x86_64 java-1.8.0-openjdk-headless.x86_64 && \
readlink -f /usr/bin/java && \
echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.372.b07-1.el7_9.x86_64' >> /root/.bashrc && \
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> /root/.bashrc && \
source ~/.bashrc
```

限制ulimit

{% content-ref url="../../../bang-zhu/debug.md" %}
[debug.md](../../../bang-zhu/debug.md)
{% endcontent-ref %}

退出，打包容器为镜像

```
docker commit bginit xiamussr/bg-b:1.0
```
