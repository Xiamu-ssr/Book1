# 搭建虚拟机集群以及安装Ambari

{% hint style="info" %}
请选择你的阵营。Linux需要更高的技巧和DeBug能力。**注意ip等根据自身更改。**
{% endhint %}

## [**Windows**](windows/+vmware-cong-tou-wan-quan-bu-shu.md) **or** [**Linux**](linux/+docker-cong-tou-wan-quan-bu-shu.md)



这应该是免费版的ambari，需要自己从源码构建，我尝试过ubuntu16.04和centos7，mvn构建不出来，而且过程很长。

{% embed url="https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.7.7" %}

看到网上很多教程包括cloudera自己家的教程，都是添加repo然后使用包管理器直接安装，比如下面这个。然后我发现，资源访问需要付费订阅？去查了一下，在21年的时候就停止免费了，但是很多教程依旧停留在免费的时代，所以一直导致安装过程停滞不前。

{% embed url="https://docs.cloudera.com/HDPDocuments/Ambari-2.5.0.3/bk_ambari-installation/content/ambari_repositories.html" %}

不过这并不难办，互联网上肯定有大量备份。比如我这份教程是按照下面这份教程，然后记录过程的。

{% embed url="https://blog.csdn.net/AnameJL/article/details/122962868" %}
