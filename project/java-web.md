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

根据需要添加依赖，组成以下pom.xml配置

<details>

<summary></summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>myproject</artifactId>
    <version>0.0.1-SNAPSHOT</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.0-SNAPSHOT</version>
    </parent>
    <!-- 将在此添加其他行... -->
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
	</dependencies>
	
    <!-- ((只有当你使用 milestone 或 snapshot 版本时，你才需要这个。)) -->
    <repositories>
        <repository>
            <id>spring-snapshots</id>
            <url>https://repo.spring.io/snapshot</url>
            <snapshots><enabled>true</enabled></snapshots>
        </repository>
        <repository>
            <id>spring-milestones</id>
            <url>https://repo.spring.io/milestone</url>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>spring-snapshots</id>
            <url>https://repo.spring.io/snapshot</url>
        </pluginRepository>
        <pluginRepository>
            <id>spring-milestones</id>
            <url>https://repo.spring.io/milestone</url>
        </pluginRepository>
    </pluginRepositories>
</project>

```



</details>

创建`src/main/java/MyApplication.java`文件并写入以下内容

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@SpringBootApplication
public class MyApplication {

    @RequestMapping("/")
    String home() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }

}
```

一个基于Maven的Java项目，需要经过以下步骤才算完整

|             |      |                              |
| ----------- | ---- | ---------------------------- |
| 验证 validate | 验证项目 | 验证项目是否正确且所有必须信息是可用的          |
| 编译 compile  | 执行编译 | 源代码编译在此阶段完成                  |
| 测试 Test     | 测试   | 使用适当的单元测试框架（例如JUnit）运行测试。    |
| 包装 package  | 打包   | 创建JAR/WAR包如在 pom.xml 中定义提及的包 |
| 检查 verify   | 检查   | 对集成测试的结果进行检查，以保证质量达标         |
| 安装 install  | 安装   | 安装打包的项目到本地仓库，以供其他项目使用        |
| 部署 deploy   | 部署   | 拷贝最终的工程包到远程仓库中，以共享给其他开发人员和工程 |

在这里，因为并不是什么大型项目，并且使用了SpringBoot CLI，只需要完成validate、compile之后就可以run了

```bash
mvn validate
mvn compile
mvn spring-boot:run
```





## 4.开发Mysql数据库

```bash
# 启动服务
service mysql start
# 使用root密码登录mysql
mysql -u root -p
> create database F;
> use F;
> exit

# 安装python和pip
apt install pip python
# 安装所需依赖
pip3 install pandas sqlalchemy pymysql openpyxl MySQLdb
```

使用以下脚本将excel表导入mysql8

```python
import pandas as pd
import os
from sqlalchemy import create_engine
import pymysql

engine = create_engine('mysql+pymysql://baby:20020730@localhost:3306/F')
work_conn_read = engine.connect()

#excel文件相对地址
df = pd.read_excel("./Festival.xlsx")
#导入数据库的表名
df.to_sql("Festival",con=work_conn_read,if_exists='append', index=False)
```
