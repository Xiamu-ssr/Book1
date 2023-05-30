---
description: 集群资源管理器
---

# YARN

## 一、hadoop yarn 简介

**Apache YARN** (Yet Another Resource Negotiator) 是 hadoop 2.0 引入的集群资源管理系统。用户可以将各种服务框架部署在 YARN 上，由 YARN 进行统一地管理和资源分配。

<figure><img src="../../../.gitbook/assets/VEB4O6@4CO0Z)}]GJP791IP.jpg" alt="" width="563"><figcaption></figcaption></figure>

## 二、YARN架构

<figure><img src="../../../.gitbook/assets/[3LLR%{[BDN43)ZMTY8Q_SG.png" alt="" width="563"><figcaption></figcaption></figure>

### 1. ResourceManager

`ResourceManager` 通常在独立的机器上以后台进程的形式运行，它是整个集群资源的主要协调者和管理者。`ResourceManager` 负责给用户提交的所有应用程序分配资源，它根据应用程序优先级、队列容量、ACLs、数据位置等信息，做出决策，然后以共享的、安全的、多租户的方式制定分配策略，调度集群资源。

### 2. NodeManager

`NodeManager` 是 YARN 集群中的每个具体节点的管理者。主要负责该节点内所有容器的生命周期的管理，监视资源和跟踪节点健康。具体如下：

* 启动时向 `ResourceManager` 注册并定时发送心跳消息，等待 `ResourceManager` 的指令；
* 维护 `Container` 的生命周期，监控 `Container` 的资源使用情况；
* 管理任务运行时的相关依赖，根据 `ApplicationMaster` 的需要，在启动 `Container` 之前将需要的程序及其依赖拷贝到本地。

### 3. ApplicationMaster

在用户提交一个应用程序时，YARN 会启动一个轻量级的进程 `ApplicationMaster`。`ApplicationMaster` 负责协调来自 `ResourceManager` 的资源，并通过 `NodeManager` 监视容器内资源的使用情况，同时还负责任务的监控与容错。具体如下：

* 根据应用的运行状态来决定动态计算资源需求；
* 向 `ResourceManager` 申请资源，监控申请的资源的使用情况；
* 跟踪任务状态和进度，报告资源的使用情况和应用的进度信息；
* 负责任务的容错。

### 4. Container

`Container` 是 YARN 中的资源抽象，它封装了某个节点上的多维度资源，如内存、CPU、磁盘、网络等。当 AM 向 RM 申请资源时，RM 为 AM 返回的资源是用 `Container` 表示的。YARN 会为每个任务分配一个 `Container`，该任务只能使用该 `Container` 中描述的资源。`ApplicationMaster` 可在 `Container` 内运行任何类型的任务。例如，`MapReduce ApplicationMaster` 请求一个容器来启动 map 或 reduce 任务，而 `Giraph ApplicationMaster` 请求一个容器来运行 Giraph 任务。

{% hint style="info" %}
Container和节点是一对多的关系。
{% endhint %}
