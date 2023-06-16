# 构建s

{% code overflow="wrap" %}
```
docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 -d --name=bgs xiamussr/bg-b:1.0 /usr/sbin/init; `
docker exec -it bgs /bin/bash
```
{% endcode %}

```
yum install chrony -y && vi /etc/chrony.conf
```

```
# 找到 server 部分，添加以下行并注释原有的server
# Use the main server as the time source
server 172.19.0.2 iburst
```

```
systemctl start chronyd && \
systemctl enable chronyd && \
systemctl status chronyd && \
chronyc sources
```

```
docker commit bgs  xiamussr/bg-s:1.0
```
