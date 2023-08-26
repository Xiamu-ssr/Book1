---
description: Ubutnu 20.04LTS-Install using the apt repository
---

# WSL安装Docker Engine

{% embed url="https://docs.docker.com/engine/install/ubuntu/" %}

## **Set up the repository**

1. Update the `apt` package index and install packages to allow `apt` to use a repository over HTTPS:

```sh
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

2. Add Docker’s official GPG key:

```sh
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

3. Use the following command to set up the repository:

```sh
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## **Install Docker Engine**

1. Update the `apt` package index:

```sh
sudo apt-get update
```

2. Install Docker Engine, containerd, and Docker Compose.

```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Verify that the Docker Engine installation is successful by running the `hello-world` image.

```sh
sudo docker run hello-world
```

{% hint style="info" %}
**sudo usermod -aG docker mumu**使普通用户可以使用docker，重新登陆并重启服务

如果还是不行，使用**sudo chmod 666 /var/run/docker.sock**
{% endhint %}
