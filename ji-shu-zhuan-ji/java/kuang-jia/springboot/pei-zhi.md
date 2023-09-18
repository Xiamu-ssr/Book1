---
description: application.properties
---

# 配置

Spring Boot是基于约定的，很多配置都有默认值，如果想使用自己的配置，可以使application.properties（或者application.yml，pro优先级>yml）文件来覆盖默认配置，比如端口号，项目路径，数据库连接等。这个文件里常用的一些配置有：

* `server.port`：指定Spring Boot内嵌容器启动的端口号，默认是8080。
* `server.servlet.context-path`：指定项目访问路径，比如`/boot`。
* `spring.datasource.*`：指定数据源的相关配置，比如驱动类，URL，用户名，密码等²。
* `spring.jpa.*`：指定JPA的相关配置，比如是否显示SQL语句，是否自动创建或更新表结构等²。
* `spring.profiles.active`：指定多环境配置，测试，生产用不同的配置文件³。
* `spring.application.name`：指定应用名称³。
* `logging.level.*`：指定日志级别，比如`logging.level.org.springframework=DEBUG`表示Spring框架的日志级别为DEBUG⁴。
* `spring.thymeleaf.*`：指定Thymeleaf模板引擎的相关配置，比如缓存，前缀，后缀等。



同时这个文件还可以写一些自定义内容，例如

```
name=abc
```
