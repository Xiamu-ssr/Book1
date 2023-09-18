# YAML

## 数据格式

* 大小写敏感
* 冒号后必须有空格
* 缩进划分层级

对象

```yaml
person:
    name: zhangsan
# 或者
person: {name: zhangsan}
```

数组

```yaml
address:
    - beijing
    - shanghai
#or
address: [beijing, shanghai]
```

常量

```yaml
msg1: 'hello \n world'#单引号忽略转义字符
msg2: "hello \n world"#双引号识别转义字符
```

参数引用

```yaml
name: alice
person:
    name: ${name}
namedouble: ${person.name}
```



## 数据读取

有以下三种方法

1. @Value
2. Environment
3. @ConfigurationProperties

以下面yaml作为例子

```yaml
##自定义
name: alice
#object
person:
  name: ${name}
  age: 20
  address: [beijing, suzhou]

#array
address: [beijing, shanghai]

#constant
msg1: 'hello \n world'
msg2: "hello \n world"
```

方式一

```java
    @Value("${name}")
    private String name;
    @Value("${person.age}")
    private int age;
    @Value("${address[0]}")
    private String address;
    @Value("${msg1}")
    private String msg1;
```

方式二

```java
    @Autowired
    private Environment env;

    @RequestMapping("")
    public String Index(){
        System.out.println(env.getProperty("name"));
        System.out.println(env.getProperty("person.name"));
        System.out.println(env.getProperty("address[1]"));
        System.out.println(env.getProperty("msg2"));
    }
```

方式三

```java
package com.example.demo.entity;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Component
@ConfigurationProperties(prefix = "person")
public class Person {
    private String name;
    private int age;
    private String[] address;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String[] getAddress() {
        return address;
    }

    public void setAddress(String[] address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", address=" + Arrays.toString(address) +
                '}';
    }
}

```
