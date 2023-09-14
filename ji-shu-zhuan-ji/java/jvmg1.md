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

{% tabs %}
{% tab title="Serial" %}
{% hint style="info" %}
分代模型年轻代GC
{% endhint %}

> A stop-of-world(STW), copying collector which uses a single GC thread.

垃圾到一定程度后，所有业务线程停止，GC开始工作。会导致Java程序运行到一定时候出现卡顿。
{% endtab %}

{% tab title="Second Tab" %}

{% endtab %}
{% endtabs %}



