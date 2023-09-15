---
description: JVM Garbage First
cover: ../../.gitbook/assets/image (18).png
coverY: 0
layout:
  cover:
    visible: true
    size: hero
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# JVMG1

Java有三个GC 算法

* Mark-Sweep标记清除
* Copying拷贝
* Mark-Compact标记压缩

Java有两种GC模型

* 分代模型
* 分区模型

<figure><img src="../../.gitbook/assets/image (19).png" alt="" width="375"><figcaption></figcaption></figure>

在这两种模型之上，Java建立了10中GC，如下图

<figure><img src="../../.gitbook/assets/image (18).png" alt="" width="563"><figcaption></figcaption></figure>

<table data-full-width="true"><thead><tr><th width="156">分代Young</th><th></th><th width="140">分代Old</th><th></th><th>分区模型</th><th></th></tr></thead><tbody><tr><td>ParNew</td><td>拷贝</td><td>CMS</td><td>标记清除</td><td>G1</td><td></td></tr><tr><td>Serial</td><td></td><td>SO</td><td></td><td>ZGC</td><td>标记压缩</td></tr><tr><td>PS</td><td>拷贝</td><td>PO</td><td></td><td>Shenandoah</td><td>标记压缩</td></tr></tbody></table>

{% tabs %}
{% tab title="Serial" %}
{% hint style="info" %}
分代模型年轻代GC
{% endhint %}

> A stop-of-world(STW), copying collector which uses a single GC thread.

垃圾到一定程度后，所有业务线程停止，GC开始工作。会导致Java程序运行到一定时候出现卡顿。
{% endtab %}

{% tab title="Parallel Scavenge" %}
{% hint style="info" %}
分代模型年轻代GC
{% endhint %}

> A stop-of-world, copying collector which uses multiple GC threads

Serial如果有太多垃圾，那么STW时间会太长，卡顿严重，可以使用多线程去回收垃圾，但是线程不是越多越好。JDK1.8默认使用PS(Parallel Scavenge)+PO(Parallel Old)。
{% endtab %}

{% tab title="CMS" %}
{% hint style="info" %}
分代模型老年代GC
{% endhint %}

> concurrent mark sweep

并发清理
{% endtab %}
{% endtabs %}



GC的标记阶段一般采用**三色标记法**，但是存在诸多bug。

<details>

<summary>其一如下</summary>

A及其子已经标记到，B被标记到但其子未标记，D还未标记，此时标记任务停止，业务任务启动

<img src="../../.gitbook/assets/image (21).png" alt="" data-size="original">

A新引用了D，B取消引用D，变成下图，此时业务任务停止，标记任务启动

![](<../../.gitbook/assets/image (22).png>)

标记任务从灰色B继续标记，发现没有子，于是一轮结束，标记AB为有效，D为垃圾。

解决方案有很多，其一如下

在JVM中设计一种屏障，一旦观察到黑色向白色建立引用，将此黑色修正为灰色。

</details>





