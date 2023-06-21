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
#列出HDFS中有损坏副本的块
hdfs fsck / -list-corruptfileblocks
#查询文件详细信息，包括哪些数据节点上有这个文件的块，以及哪些块是损坏的等等
hdfs fsck /path/to/corrupt/file -locations -blocks -files
#删除所有已经missing的块
hdfs fsck -delete
```

```bash
# 连接hive
beeline -u jdbc:hive2://<ip>:<port> -n hive -p hive
```
