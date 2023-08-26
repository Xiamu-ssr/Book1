# Maven

{% hint style="info" %}
以下是Java SE版本号和主要版本对应关系的列表：

* Java SE 1.1 对应 JDK 1.1.x
* Java SE 1.2 对应 JDK 1.2.x
* Java SE 1.3 对应 JDK 1.3.x
* Java SE 1.4 对应 JDK 1.4.x
* Java SE 5 对应 JDK 1.5.x
* Java SE 6 对应 JDK 1.6.x
* Java SE 7 对应 JDK 1.7.x
* Java SE 8 对应 JDK 1.8.x
* Java SE 9 对应 JDK 9.x
* Java SE 10 对应 JDK 10.x
* Java SE 11 对应 JDK 11.x
* Java SE 12 对应 JDK 12.x
* Java SE 13 对应 JDK 13.x
* Java SE 14 对应 JDK 14.x
* Java SE 15 对应 JDK 15.x
* Java SE 16 对应 JDK 16.x
* Java SE 17 对应 JDK 17.x
{% endhint %}

`mvn archetype:generate -DgroupId=com.example -DartifactId=my-app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false`创建一个基本的Maven项目，其中包括一个Java类和一个测试类

`mvn dependency:purge-local-repository`清空Maven的本地仓库缓存，强制Maven重新下载项目依赖的所有库

`mvn package`重新编译、测试、打包项目，并将生成的构件存放到本地仓库中。
