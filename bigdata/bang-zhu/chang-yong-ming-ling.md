# 常用命令

```sh
#查看某个用户属于哪些组
hdfs groups user
#查看某个组有哪些用户
#在namenode上
getent group g
```

```sh
# 查看YARN目前所有任务
yarn application -list
#查看各个节点YARN状态
yarn node -list
```

```bash
#检查集群状态
hdfs dfsadmin -report
#检查某个文件或文件夹在hdfs上是否健康
hadoop fsck path
```
