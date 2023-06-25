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

### 3.1 初始化项目

查看软件版本然后在下面的网站下载初始项目文件夹并移入容器

{% embed url="https://start.springboot.io/" %}

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

在这里，因为并不是什么大型项目，并且只需要在本地部署，同时又使用了SpringBoot CLI，所以只需要完成validate、compile、package之后就可以run了

```bash
mvn dependency:tree
mvn validate
mvn compile
mvn package
mvn spring-boot:run
```

### 3.2 项目模块和依赖

设计初期，划分出2个配置文件和4个Java核心文件，如下

* java/demo/pom.xml

Maven项目开发工具配置文件，可指定各种依赖库、插件等配置

* java/demo/src/main/resources/application.properties

Spring Boot 应用程序的配置文件，可指定数据库连接信息、服务器端口等等配置

* java/demo/src/main/java/com/example/demo/Festival.java

Festival表实体类，属性和Mysql的Festival结构对应，还包括构造方法和 Getter/Setter 方法，用于存储来自mysql表的数据。

* java/demo/src/main/java/com/example/demo/FestivalRepository.java

Festival接口，继承自JpaRepository，基于Festival类可以对Mysql表实行各类操作。

* java/demo/src/main/java/com/example/demo/FestivalController.java

处理前端的请求，通过FestivalRepository各类操作，完成请求所需数据，处理后将结果返回给前端

* java/demo/src/main/java/com/example/demo/DemoApplication.java

Spring Boot web入口程序

### 3.3 项目层次

<img src="../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">

### 3.4项目细节解析

#### 3.4.1 pom.xml

项目配置继承自Spring Boot的一个父项目，是使用Spring Boot框架的起手式。

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.5.2</version>
    <relativePath/>
</parent>
```

添加依赖，用于构建 Web 应用程序的 Spring Boot Starter，属于Spring Boot Web的起手式。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

添加依赖，用于编写单元测试和集成测试的 Spring Boot Starter，属于Spring Boot Web的起手式。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>org.junit.vintage</groupId>
            <artifactId>junit-vintage-engine</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

添加依赖，MySQL JDBC 驱动程序，用于与 MySQL 数据库进行交互。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.25</version>
</dependency>
```

添加依赖，用于 Spring Boot 应用程序中使用 JPA 进行数据库操作。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

3.4.2&#x20;

```properties
# 数据库连接信息
spring.datasource.url=jdbc:mysql://localhost:3306/F
spring.datasource.username=baby
spring.datasource.password=20020730

# java后端监听端口和ip
server.port=8080
server.address=127.0.0.1

spring.jpa.hibernate.ddl-auto=update
```

细节也许可以不用讲

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
