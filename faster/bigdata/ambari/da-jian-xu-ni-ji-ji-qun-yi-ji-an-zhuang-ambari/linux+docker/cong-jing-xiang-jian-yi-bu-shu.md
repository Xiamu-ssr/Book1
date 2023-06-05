# 从镜像简易部署

### 1. 拉取镜像

```sh
docker pull xiamussr/bigdata-slave:1.0
docker pull xiamussr/bigdata-master:1.0
```

### 2. 创建虚拟网络

```sh
docker network create bigdata --subnet=172.19.0.0/16 --gateway=172.19.0.1
docker network list #查看所有网络
docker network inspect bigdata #查看bigdata网络详细信息
```

### 3. 创建容器

```
docker run --network bigdata --ip 172.19.0.2 -p 8080:8080 \
 --name bg-c79-0 -it --cpus=6 -m 16G --privileged=true \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock \
   --stop-signal=RTMIN+3 \
   xiamussr/bigdata-master:1.0 /usr/sbin/init
```

```sh
docker run --network bigdata --ip 172.19.0.3 --name bg-c79-1 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.4 --name bg-c79-2 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.5 --name bg-c79-3 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
docker run --network bigdata --ip 172.19.0.6 --name bg-c79-4 -it --cpus=4 -m 12G --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro --tmpfs /run --tmpfs /run/lock --stop-signal=RTMIN+3 xiamussr/bigdata-slave:1.0 /usr/sbin/init
```

### 4. 集群通信

写好/etc/hosts，发送给每个slave。

执行脚本配置互相免密。

