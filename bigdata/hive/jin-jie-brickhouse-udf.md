# 进阶-Brickhouse UDF

仓库地址

{% embed url="https://github.com/klout/brickhouse" %}

或者可以直接从第三方下载jar

{% embed url="https://mvnrepository.com/artifact/com.klout/brickhouse/0.6.0" %}

{% embed url="https://jar-download.com/artifacts/com.klout/brickhouse/0.6.0" %}

把brickhouse.jar上传到服务器。

```bash
#列出 brickhouse.jar 文件中的所有文件和目录
jar tf brickhouse.jar
#从brickhouse.jar文件中提取brickhouse.hql文件，并将其保存在当前目录中
jar xf brickhouse.jar brickhouse.hql
#进入hive命令行后,加载所有UDF为临时UDF
SOURCE /path/to/brickhouse.hql;
```

{% hint style="info" %}
注意文件和文件夹权限问题
{% endhint %}
