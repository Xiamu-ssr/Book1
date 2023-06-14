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

