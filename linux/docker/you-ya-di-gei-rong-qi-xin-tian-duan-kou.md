# 优雅地给容器新添端口

一共分为三步，停止容器和docker服务，修改配置文件，重启服务和容器。

这里只讲如何修改配置文件。

## 如果你是Linux环境

容器配置文件`hostconfig.json` 通常位于 `/var/lib/docker/containers/[hash_of_the_container]/hostconfig.json` 或者 `/var/snap/docker/common/var-lib-docker/containers/[hash_of_the_container]/hostconfig.json`

找到`PortBindings`字段，以下是一个端口的格式例子

```
"PortBindings": {
                "8080/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "8080"
                    }
                ],
                "8088/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "8088"
                    }
                ]
            },
```

## 如果你是windws+wsl2环境

那么你需要修改两个文件，`hostconfig.json`和`config.v2.json`，它们都位于`/mnt/wsl/docker-desktop-data/data/docker/<containerID>`下。

`hostconfig.json`文件修改和linux的一样。

`config.v2.json`需要修改以下两个字段

```
"ExposedPorts":{"8080/tcp":{},"8088/tcp":{}}

"Ports":{"8080/tcp":[{"HostIp":"0.0.0.0","HostPort":"8080"}],"8088/tcp":[{"HostIp":"0.0.0.0","HostPort":"8088"}]}
```

