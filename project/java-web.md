# Java-Web

## 1. 配置列表

|      |                    |
| ---- | ------------------ |
| OS   | Ubuntu 22.04 LTS   |
| Java | openJDK 8          |
| 构建工具 | Maven              |
| 部署工具 | Docker             |
| 前端框架 | Vue + Element-plus |
| 后端框架 | SpringBoot         |
| 数据库  | Mysql              |

## 2. 环境配置

```bash
#安装java
apt install openjdk-17-jdk
#安装maven
apt install maven
#安装gradle
apt install gradle
#安装SDKMAN
curl -s "https://get.sdkman.io" | bash
#安装SpringBoot CLI
sdk install springboot
```

## 3.开发Java后端

查看软件版本然后在下面的网站下载初始项目文件夹并移入容器

{% embed url="https://start.springboot.io/" %}

## 4.开发Mysql数据库

```bash
# 启动服务
service mysql start
```
