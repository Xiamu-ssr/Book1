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
docker run --network bigdata --ip 172.19.0.3 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs1 xiamussr/bg-b:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}

{% tab title="2" %}
{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.4 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs2 xiamussr/bg-b:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}

{% tab title="3" %}
{% code overflow="wrap" %}
```
docker run --network bigdata --ip 172.19.0.5 --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs3 xiamussr/bg-b:1.0 /usr/sbin/init ; `
docker ps -a
```
{% endcode %}
{% endtab %}
{% endtabs %}
