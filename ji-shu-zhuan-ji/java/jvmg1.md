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

Java有三个基础GC 算法

<table><thead><tr><th width="239"></th><th></th></tr></thead><tbody><tr><td>Mark-Sweep标记清除</td><td><p>它分为两个阶段：标记和清除。</p><p>标记阶段会遍历所有可达的对象，并将它们标记为存活。清除阶段会删除所有未被标记的对象，即垃圾对象。</p><p>这种算法的优点是实现简单，不需要额外的空间。缺点是会产生内存碎片，导致后续分配大对象时可能失败。</p></td></tr><tr><td>Copying拷贝</td><td><p>一种将内存分为两个相等的区域，每次只使用其中一个区域的算法。当这个区域快要用完时，就会将存活的对象复制到另一个区域，并清空原来的区域。</p><p>这种算法的优点是不会产生内存碎片，且复制过程中不需要暂停应用程序。缺点是浪费了一半的内存空间，且复制大量对象时会影响性能</p></td></tr><tr><td>Mark-Compact标记压缩</td><td><p>一种结合了标记清除和拷贝算法的思想的算法。它也分为两个阶段：标记和压缩。</p><p>标记阶段和标记清除算法相同，都是遍历所有可达的对象，并将它们标记为存活。压缩阶段则是将所有存活的对象向内存空间的一端移动，并更新它们的引用地址。</p><p>这种算法的优点是既不会浪费内存空间，又不会产生内存碎片。缺点是移动对象和更新引用地址时需要暂停应用程序。</p></td></tr></tbody></table>

Java有两种GC模型

* 分代模型
* 分区模型

<figure><img src="../../.gitbook/assets/image (19).png" alt="" width="375"><figcaption></figcaption></figure>

在这两种模型之上，Java建立了10中GC，如下图

<figure><img src="../../.gitbook/assets/image (18).png" alt="" width="563"><figcaption></figcaption></figure>

<table data-full-width="true"><thead><tr><th width="156">分代Young</th><th></th><th width="140">分代Old</th><th></th><th>分区模型</th><th></th></tr></thead><tbody><tr><td>ParNew</td><td>Copying</td><td>CMS</td><td>Mark-Sweep</td><td>G1</td><td>Copying和Mark-Compact</td></tr><tr><td>Serial</td><td>Copying或Mark-Compact</td><td>SO</td><td>Mark-Compact</td><td>ZGC</td><td>Copying和Mark-Compact</td></tr><tr><td>PS</td><td>Copying</td><td>PO</td><td>Mark-Compact</td><td>Shenandoah</td><td>Copying和Mark-Compact</td></tr></tbody></table>

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



GC的标记阶段一般采用**三色标记法**，但是存在诸多bug，同时也会提到CMS对其解决方案。

<details>

<summary>其一如下</summary>

A及其子已经标记到，B被标记到但其子未标记，D还未标记，此时标记任务停止，业务任务启动

<img src="../../.gitbook/assets/image (21).png" alt="" data-size="original">

A新引用了D，B取消引用D，变成下图，此时业务任务停止，标记任务启动

![](<../../.gitbook/assets/image (22).png>)

标记任务从灰色B继续标记，发现没有子，于是一轮结束，标记AB为有效，D为垃圾。

解决方案有很多，其一如下

在JVM中设计一种屏障，一旦观察到黑色向白色建立引用，将此黑色修正为灰色。这就是CMS对三色标记的修正方案，称为Incremental Update，不过这种方案仍然有非常隐秘的问题，比如A有属性1，2，标记任务将1标记完后，2还没标记，中止切换到业务任务，将1引用

</details>





