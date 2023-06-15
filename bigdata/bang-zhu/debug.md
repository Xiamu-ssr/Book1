# QA

## Ambari

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

## Hadoop

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

## Hive3

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
