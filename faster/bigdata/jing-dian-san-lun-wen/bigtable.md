---
description: A Distributed Storage System for Structured Data浅读，标注
---

# BigTable

{% embed url="https://static.googleusercontent.com/media/research.google.com/zh-CN/archive/bigtable-osdi06.pdf" %}
BigTable PDF
{% endembed %}

## 1.Introduction

Bigtable旨在管理结构化数据，并具有可靠的可扩展性、高性能和高可用性等特点

## 2.Data Model

Bigtable是一种用于管理结构化数据的分布式存储系统，它将数据组织为稀疏的、分布式的、持久的多维排序映射。这个map由行键、列键和时间戳进行索引，每个值都是一个未解释的字节数组。
