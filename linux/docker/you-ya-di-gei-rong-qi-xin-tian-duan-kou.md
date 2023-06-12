# 优雅地给容器新添端口

`docker inspect <container_name>`查看容器信息，找到**`HostConfig`**可以看到port映射

1. Stop the container (`docker stop <container_name>`).
2. Stop docker service (per Tacsiazuma's comment)
3. Change the file.

容器配置文件`hostconfig.json` 通常位于 `/var/lib/docker/containers/[hash_of_the_container]/hostconfig.json` 或者 `/var/snap/docker/common/var-lib-docker/containers/[hash_of_the_container]/hostconfig.json`

{% hint style="info" %}
如果你是docker desktop for windows(wsl2)，那么文件位于wsl2 。

`docker-desktop-data\data\docker\containers\`
{% endhint %}

4. Restart your docker engine (to flush/clear config caches).
5. Start the container (`docker start <container_name>`).
