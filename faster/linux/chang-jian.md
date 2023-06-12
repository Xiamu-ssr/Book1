# 常见

## 常用软件包

像docker镜像这种，拉下来只有几十MB的，什么软件都没有，每次都需要自己缺少啥才想起来手动apt install

```sh
apt update && apt install vim sudo proxychains4 net-tools git wget curl htop openssh openssh-server
```

## 用户相关

```sh
#创建新用户并赋予sudo权限
adduser mumu && usermod -aG sudo mumu
#查看用户属于哪些组
groups user
#查看一个组里都有哪些用户
getent group g
```

## CentOS

{% embed url="https://vault.centos.org/" %}
历届版本iso下载,isos/
{% endembed %}

{% embed url="http://mirror.centos.org/centos/7/os/x86_64/" %}
官方镜像站点
{% endembed %}
