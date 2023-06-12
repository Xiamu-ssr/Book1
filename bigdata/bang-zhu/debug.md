# QA

<details>

<summary>Error occured during stack advisor command invocation: Cannot create /var/run/ambari-server/stack-recommendations</summary>

查看`/etc/ambari-server/conf/ambari.properties`文件中的`ambari-server.user`属性，确定您运行ambari-server的用户名。 修改/var/run/ambari-server目录的用户为上一步的用户名，例如：`chown -R ambari /var/run/ambari-server`。

</details>

<details>

<summary>容器重启后需要注意的一系列问题</summary>

首先是/etc/hosts的问题，容器重启后会被重置，建议备份，写入.bashrc自动恢复。

然后是想要ambari-server restart前需要重新setup一遍

最后是需要重启所有ambari-agent。

```sh
## bk hosts
yes | cp -i /etc/hosts.bk /etc/hosts
bash /root/Shell/scp_to_all.sh /etc/hosts /etc
```

</details>

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
