---
description: source 2023/05/28。小记、琐事、随笔。
---

# 日常小记

<details>

<summary>2023/05</summary>

#### 28

终于在本地用虚拟机安装好了ambari，命令`hadoop fs -ls /`有反应，努力没有白费，只装了一个HDFS，YARN因为内存不够，坐等32\*2内存条到货。

#### 29

速通了一遍maven，并且用github搭建了远程私人maven仓库。

#### 30

浅读了一番大数据的经典三论文，google确实6。看了HDFS，MapReduce和YARN看了一部分

#### 31

看完了YARN，内存条到了，出了点问题，重装了系统，win11，配了环境。

</details>

<details>

<summary>2023/06</summary>

#### 1

配环境，旧磁盘识别不到了，需要硬盘盒当做U盘接入。配WSL。重现搭建hadoop集群，这次要开5个！！虚拟机

#### 2

5个虚拟机，部署出来了！enjoy :-)，打算去学校服务器用docker试试。本机核太少了qwq。

#### 3

看了一些hive。实操了Linux+Docker搭建hadoop集群。

<img src="../../.gitbook/assets/(&#x60;J}7RYP}I0Y26GVUVF03GK.png" alt="" data-size="original">

#### 4

比了icpc丝绸之路，银奖到手。不过太早，睡眠不足。今天linuxdocker安装hive出现了玄学bug，hive get不到mysql配置页面。。。然后ambari server restart莫名其妙把ambari集群配置重置了？？？nothing left，然后重新装的时候，在一开始选择hive就可以装上，是时候重新来一遍了，一定要记得打包传docker hub。windowsVM就可以get到mysql，但是呢？连不上。oh shit。linuxdocker hive可以用了，不错不错。

**5**

重新搞了一遍linux+docker部署hadoop，并且录了视频，发到了b站。知乎，csdn也相继更新。

从bigdata-base镜像做了主节点和从节点镜像，下次部署linux+docker就更方便了。

</details>
