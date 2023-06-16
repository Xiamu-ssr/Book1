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

导入Shell脚本文件夹

```
docker cp .\Shell\ bgm:/root; `
docker exec -it bgm /bin/bash
```

修改config.sh和/etc/hosts后，配置免密

```
bash scp_to_all.sh /etc/hosts /etc && \
bash scp_to_all.sh /root/Shell /root && \
bash ssh_all_to_all.sh
```

给从节点配置ntp

```
echo -e "bgs1\nbgs2\nbgs3" > host.txt && \
pssh -h host.txt -i yum install -y ntpdate && \
pssh -h host.txt ntpdate bgm && \
echo "29,59 * * * * /usr/sbin/ntpdate bgm" > tmp.txt && \
pssh -h host.txt -t 10 -I < tmp.txt 'crontab -' && \
pssh -h host.txt -i date && \
pssh -h host.txt systemctl start ntpdate && \
pssh -h host.txt systemctl enable ntpdate && \
pssh -h host.txt -i date
```
