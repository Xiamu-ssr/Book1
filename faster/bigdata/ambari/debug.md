# DeBug

<details>

<summary>Error occured during stack advisor command invocation: Cannot create /var/run/ambari-server/stack-recommendations</summary>

查看`/etc/ambari-server/conf/ambari.properties`文件中的`ambari-server.user`属性，确定您运行ambari-server的用户名。 修改/var/run/ambari-server目录的用户为上一步的用户名，例如：`chown -R ambari /var/run/ambari-server`。

</details>

<details>

<summary>容器重启后需要注意的一系列问题</summary>

首先是/etc/hosts的问题，容器重启后会被重置，建议备份，写入.bashrc自动恢复。

然后是想要ambari-server start前需要重新setup一遍

</details>
