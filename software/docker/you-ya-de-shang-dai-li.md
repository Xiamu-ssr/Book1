# 优雅的上代理

docker代理分为两种，容器代理和daemon代理。

## 容器代理

在 `~/.docker/config.json` 文件中，设置代理环境变量。

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://127.0.0.1:1080",
      "httpsProxy": "http://127.0.0.1:1080",
      "noProxy": "*.local, 169.254/16"
    }
  }
}
```

```sh
sudo systemctl restart docker
```

或者你也可以通过端口让容器使用host代理。

## daemon代理

Docker daemon是`docker pull`和`docker push`的实际执行者，所以不能简单的像proxychains4这样代理。

1. 在 `/etc/systemd/system` 目录下创建 `docker.service.d` 目录，并在该目录下创建`proxy.conf` 文件
2. 在 `proxy.conf` 文件中添加你的代理信息，例如：

```
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

3. 刷新更改并重新启动 Docker 服务。

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

{% hint style="info" %}
这个网址支持pull代理
{% endhint %}

{% embed url="https://dockerproxy.com/" %}
