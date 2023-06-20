# QA

### Ambari

<details>

<summary>Error occured during stack advisor command invocation: Cannot create /var/run/ambari-server/stack-recommendations</summary>

查看`/etc/ambari-server/conf/ambari.properties`文件中的`ambari-server.user`属性，确定您运行ambari-server的用户名。 修改/var/run/ambari-server目录的用户为上一步的用户名，例如：`chown -R ambari /var/run/ambari-server`。

</details>

<details>

<summary>容器重启后需要注意的一系列问题</summary>

首先是/etc/hosts的问题，容器重启后会被重置，建议备份。

然后是想要ambari-server restart前需要重新setup一遍

最后是需要重启所有ambari-agent。

写一个脚本，每天第一次启动执行一下

```sh
#init.sh
yes | cp -i /etc/hosts.bk /etc/hosts
bash /root/Shell/scp_to_all.sh /etc/hosts /etc

ambari-server setup --jdbc-db=mysql --jdbc-driver=/usr/share/java/mysql-connector-java.jar
pssh -h /root/Downloads/host.txt ambari-agent restart
ambari-server restart
```

</details>

<details>

<summary>ambari的CRIT之Ulimit for open files (-n) is 800000 which is higher or equal than critical value of 800000</summary>

#### 临时方案

```bash
ulimit -n 800000
```

#### 永久方案

```bash
sudo vi /etc/security/limits.conf
#写入或修改为
* soft nofile 1000000
* hard nofile 1000000
# 退出后让系统重新加载配置文件
sudo sysctl -p
```

</details>

### HDFS

<details>

<summary>怎么给hdfs新建一个用户，并且有基本的权限。</summary>

```bash
# 在Linux系统上创建user1，并加入到hadoop组
useradd mumu -G hadoop
#把mumu加入hdfs组
usermod -aG hdfs mumu

# 在hdfs的/user目录下创建user1的主目录
su - hdfs -c "hdfs dfs -mkdir /user/mumu"

# 修改user1主目录的所有者和权限
su - hdfs -c "hdfs dfs -chown mumu:hadoop /user/mumu"
su - hdfs -c "hdfs dfs -chmod 755 /user/mumu"

# 刷新namenode的用户和组的映射
hdfs dfsadmin -refreshUserToGroupsMappings

```

</details>

<details>

<summary>怎么查看一个文件在hdfs被分成多少块，每个块的位置</summary>

```
hdfs fsck /path/to/file -files -blocks -locations
```

`hdfs fsck`命令用于检查Hadoop分布式文件系统(HDFS)中特定路径下的文件和目录的健康状态。除了 `-files`，`-blocks`和`-locations`参数外，还有其他一些可用的参数，这些参数的含义如下：

* `-openforwrite`: 仅检查当前正在写入或打开以进行写入操作的块。
* `-list-corruptfileblocks`: 列出所有已损坏的块及其所在文件的详细信息。
* `-move`: 将损坏的块移动到垃圾桶，以便稍后进行进一步分析。
* `-delete`: 删除所有已损坏的块。
* `-files -blocks -locations`: 分别列出文件、块和块的位置信息。

`-files`参数用于列出指定路径下的所有文件及其相关信息，包括文件大小、块大小、副本数等。

`-blocks`参数用于列出指定路径下每个文件的所有块及其相关信息，如块ID、块大小、副本位置等。

`-locations`参数用于列出指定路径下每个块的副本位置信息，包括数据节点的IP地址和端口号。

</details>

### MapReduce

<details>

<summary>mapreduce check test finish 100% but error end with Unknown Job</summary>

If the job fails with unknown job exception frequently , disable the log aggregation for YARN.

The following steps will disable the log aggregation

1\. Login to Ambari

2\. Select YARN -> Configs ->Advanced

3\. Uncheck Enable Log Aggregation.

4\. Restart YARN and all the dependent services.

</details>

### Hive3

<details>

<summary>怎么从0到1，弄出第一个管理员</summary>

如果你使用ambari安装的hive，那么请在ambari web ui中设置hive的config，key和value对应如下：

如果你可以直接修改hive-site.xml就能起作用，那么使用对应格式设置如下key和value：

```
hive.server2.enable.doAs=false
hive.security.authorization.enabled=true
hive.security.authorization.manager=org.apache.hadoop.hive.ql.security.authorization.plugin.sqlstd.SQLStdHiveAuthorizerFactory
hive.security.authenticator.manager=org.apache.hadoop.hive.ql.security.SessionStateUserAuthenticator
hive.users.in.admin.role=<admin user>
```

```xml
  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>
  <property>
    <name>hive.security.authorization.enabled</name>
    <value>true</value>
  </property>
  <property>
    <name>hive.security.authorization.manager</name>
    <value>org.apache.hadoop.hive.ql.security.authorization.plugin.sqlstd.SQLStdHiveAuthorizerFactory</value>
  </property>
  <property>
    <name>hive.security.authenticator.manager</name>
    <value>org.apache.hadoop.hive.ql.security.SessionStateUserAuthenticator</value>
  </property>
  <property>
    <name>hive.users.in.admin.role</name>
    <value>hive</value>
  </property>
```

\<admin user>用英文逗号,分割

然后beeline使用admin user登录，在命令行中输入以下即可将当前用户设置为管理员

```sql
set role ADMIN;
```

查看当前用户角色

```sql
show current role;
```

**参考资料**

[https://community.cloudera.com/t5/Support-Questions/hive-with-SQL-Standard-based-Authorization/td-p/111505](https://community.cloudera.com/t5/Support-Questions/hive-with-SQL-Standard-based-Authorization/td-p/111505)

[https://stackoverflow.com/questions/30080203/grant-permission-in-hive](https://stackoverflow.com/questions/30080203/grant-permission-in-hive)

</details>

<details>

<summary>Metastore Authorization api invocation for remote metastore is disabled in this configuration.Run commands via jdbc/odbc clients via HiveServer2 that is using embedded metastore.</summary>

正在使用embedded metastore，而不是独立的metastore，这将无法使用授权命令。

`hive.security.metastore.authorization.manager`参数中，值`org.apache.hadoop.hive.ql.security.authorization.StorageBasedAuthorizationProvider`授权管理器提供了基于Hive存储层的授权机制，可以通过Hive CLI或HiveServer2接口进行授权操作。而`org.apache.hadoop.hive.ql.security.authorization.MetaStoreAuthzAPIAuthorizerEmbedOnly`授权管理器则提供了基于SQL语句的授权机制，并且只能通过Metastore API进行授权操作，无法通过Hive CLI或HiveServer2接口进行授权操作。

beeline属于Hive CLI或HiveServer2接口。

移除`org.apache.hadoop.hive.ql.security.authorization.MetaStoreAuthzAPIAuthorizerEmbedOnly`然后重启服务即可

</details>

<details>

<summary>SemanticException Invalid path '"/root/HiveTest/emp.txt"': No files matching path </summary>

文件存在，被说不存在，一般是因为beeline里的用户对这个文件没有权限。

</details>

<details>

<summary>Error: The file that you are trying to load does not match the file format of the destination table. </summary>



</details>
