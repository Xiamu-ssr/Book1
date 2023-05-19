---
description: 可迁移式部署
---

# 部署指导

## 获取镜像

首先docker把镜像tar加载进去，使用`docker imges -a`查看所有镜像

## 初次启动

提供初次启动脚本，`bash init.sh`即可，具体原理细节如下

{% tabs %}
{% tab title="config.sh" %}
```sh
web=xiamussr/qhubl:1.2
mysql=xiamussr/qhubl-mysql:1.0
admin=xiamussr/qhubl-admin:1.0
```

这个config.sh设置了三个镜像的名称和标签&#x20;
{% endtab %}

{% tab title="init.sh" %}
```sh
source ./config.sh
docker network create qhubl --subnet=172.19.0.0/16 --gateway=172.19.0.1
docker run --network qhubl --ip 172.19.0.2 -p 3306:3306 --name mysql -d --restart=always -v /auroras/mysql/log:/var/log/mysql -v /auroras/mysql/data:/var/lib/mysql -v /auroras/mysql/conf:/etc/mysql/conf.d  -e MYSQL_ROOT_PASSWORD=Aa4115252397 $mysql
docker run --network qhubl --ip 172.19.0.3 -p 8888:8888 --name admin -d $admin
docker run --network qhubl --ip 172.19.0.4 -p 5173:5173 -p 5050:5050 --name web -itd $web

web_id=$(docker ps -a | grep $web | awk '{print $1}')
docker exec $web_id bash /root/start.sh
```

这个为启动脚本，首先获取config.sh的变量。

第二行创建一个docker network小局域网。

第三四五行从镜像中创建容器，并把容器并入这个小局域网，使得它们之间可以通过ip通信，同时向主机开放端口，方便外部访问。

最后两行为web容器启动服务命令，另外两个容器在启动时会自动启动服务。
{% endtab %}
{% endtabs %}

## 暂停

提供暂停脚本，`bash stop.sh`即可，具体原理细节如下

{% tabs %}
{% tab title="stop.sh" %}
```sh
source ./config.sh

web_id=$(docker ps -a | grep $web | awk '{print $1}')
mysql_id=$(docker ps -a | grep $mysql | awk '{print $1}')
admin_id=$(docker ps -a | grep $admin | awk '{print $1}')

docker stop $web_id
docker stop $mysql_id
docker stop $admin_id
```

获取三个容器的id，然后依次暂停它们
{% endtab %}
{% endtabs %}

## 二次启动

提供二次启动脚本，`bash start.sh`即可，具体原理细节如下

{% tabs %}
{% tab title="start.sh" %}
```sh
source ./config.sh

web_id=$(docker ps -a | grep $web | awk '{print $1}')
mysql_id=$(docker ps -a | grep $mysql | awk '{print $1}')
admin_id=$(docker ps -a | grep $admin | awk '{print $1}')

docker start $web_id
docker start $mysql_id
docker start $admin_id
```

获取三个容器的id，然后依次启动它们
{% endtab %}
{% endtabs %}
