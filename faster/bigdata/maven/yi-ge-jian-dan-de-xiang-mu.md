---
description: 速通
---

# 一个简单的项目

### 配置环境

安装JDK，安装maven，VSCode安装maven插件。

### 创建项目

选择快速模式，然后根据提示选择，不知道的就默认。

<figure><img src="../../../.gitbook/assets/AQ[I(V72%GKZKY&#x60;F4X3X3MB.png" alt="" width="563"><figcaption></figcaption></figure>

### 编写代码

在 src/main/java 目录下创建一个名为 `Addition.java` 的 Java 类，实现计算两个整数相加的功能。代码如下：

```java
public class Addition {
    public int add(int a, int b) {
        return a + b;
    }
}
```

### 编写测试代码

在 src/test/java 目录下创建一个名为 `AdditionTest.java` 的 Java 类，使用 JUnit 框架进行单元测试。代码如下：

```java
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class AdditionTest {
    @Test
    public void testAdd() {
        Addition addition = new Addition();
        int sum = addition.add(2, 3);
        assertEquals(5, sum);
    }
}
```

### 配置 Maven 依赖

在项目的 pom.xml文件中，需要添加 JUnit 的依赖，以便在编译和测试时自动下载和引入 JUnit。在 `<dependencies>` 元素中添加以下代码：

```xml
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.13.2</version>
    <scope>test</scope>
</dependency>
```

### 验证代码

`mvn validate`该命令会检查项目的基本信息是否正确，包括 pom.xml 文件中的元素是否正确，是否存在必要的依赖关系等。如果没有错误信息，则表示验证成功。

### 编译代码

`mvn compile`该命令会编译项目的 Java 代码，并将编译结果保存在 target/classes 目录下。

### 运行测试

`mvn test`该命令会运行项目的测试代码，包括 `AdditionTest.java`。如果所有的测试都通过，则表示测试成功。

### 打包项目

`mvn package` 该命令会将项目打包成一个 JAR 文件，保存在 target 目录下。在本例中，JAR 文件的名称为 `addition-1.0-SNAPSHOT.jar`。

### 检查项目

`mvn verify`该命令会检查项目的打包结果是否正确，包括 JAR 文件的内容是否正确、是否存在必要的文件等。如果没有错误信息，则表示检查成功。

### 安装项目

`mvn install`该命令会将项目安装到本地 Maven 仓库中，以便其他项目可以引用它。在本例中，安装后的 JAR 文件路径为 `~/.m2/repository/com/example/addition/1.0-SNAPSHOT/addition-1.0-SNAPSHOT.jar`。

### 部署项目

`mvn deploy`该命令会将项目部署到指定的远程仓库中。在执行该命令之前，需要在 pom.xml 文件中配置远程仓库的信息。
