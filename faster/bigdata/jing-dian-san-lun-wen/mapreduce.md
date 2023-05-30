---
description: Simplified Data Processing on Large Clusters，浅读，标注
---

# MapReduce

{% embed url="https://static.googleusercontent.com/media/research.google.com/zh-CN/archive/mapreduce-osdi04.pdf" %}
MapReduce PDF
{% endembed %}

## 1.Introduction

输入数据通常很大时，计算必须分布在数百或数千台机器上，以便在合理的时间内完成。但是如何并行化计算、分布数据和处理故障等问题，使得原本简单的计算用大量复杂的代码来处理这些问题变得模糊不清。作为对这种复杂性的反应，我们设计了新的抽象，它允许我们表达我们试图执行的简单计算，但隐藏了库中并行化，容错，数据分布和负载平衡的混乱细节。这就是map和reduce。

## 2.Programming Model

MapReduce的基本思想是，用户只需要定义两个函数：map函数和reduce函数。map函数负责对输入数据进行过滤和排序，将数据转换成键值对的形式。reduce函数负责对map函数产生的键值对进行汇总和处理，输出最终结果。

基于MapReduce模型的任务，除了单词统计，还有许多有趣的例子，字符串匹配，URL访问频率，网页链接图，文档关键词统计，倒排索引（文档的单词作为key，文档id作为value，可以快速定位单词的位置。），分布式排序。

## 3.Implementation

MapReduce的工作流程，分为以下几个步骤：

1. 用户程序首先将输入文件切分成M个小块，每个小块的大小通常为16MB到64MB（用户可以通过参数控制）。然后在一个服务器集群中启动多个程序的副本。其中一个副本是特殊的，称为master，负责分配和监控任务。其他的副本是workers，负责执行map或reduce任务。总共有M个map任务和R个reduce任务。
2. master选择空闲的workers，并分配给它们一个map任务或一个reduce任务。一个worker被分配了一个map任务后，就会读取对应的输入文件块的内容，并将其解析成键值对，然后传递给用户定义的map函数。map函数产生的中间键值对会缓存在内存中。
3. 周期性地，缓存中的键值对会被写入到本地磁盘上，并按照一定的规则划分成R个区域。这些键值对在本地磁盘上的位置会被传回给master，master负责将这些位置转发给reduce workers。
4. 当一个reduce worker收到master通知时，它会通过远程调用从map workers的本地磁盘上读取缓存的数据。当一个reduce worker读取完所有的中间数据后，它会对数据按照键进行排序，以便将相同键的值放在一起。排序是必要的，因为通常很多不同的键会映射到同一个reduce任务。如果中间数据太大，无法放在内存中，则需要使用外部排序。
5. reduce worker遍历排序后的中间数据，并对每个唯一的键及其对应的值集合调用用户定义的reduce函数。reduce函数输出的结果会追加到最终输出文件中。
6. 当所有的map任务和reduce任务都完成后，master会唤醒用户程序。此时，MapReduce调用在用户程序中返回。执行成功后，MapReduce产生的输出结果会保存在R个输出文件中（每个reduce任务一个文件，文件名由用户指定）。通常情况下，用户不需要将这些输出文件合并成一个文件——他们可以将这些文件作为另一个MapReduce调用或其他分布式应用程序的输入。

### 3.3Fault Tolerance

Worker Failure：master定期ping每个worker，如果worker没有回应，master将其标记为失效，并回收这个worker负责的任务分配到其它worker上。

Master Failure：如果master fail，可以从上一个检查点状态开始新的副本。然而，考虑到只有一个master，它的失败是不可能的;因此，如果master失败，我们会中止MapReduce计算。

MapReduce计算框架具有容错能力，可以处理不同类型的故障，包括崩溃故障、遗漏故障和任意故障。MapReduce的容错机制主要依赖于map和reduce任务输出的原子提交，以及master和worker之间的心跳检测。

### 3.4Locality

网络带宽是稀缺资源，所以我们使用GFS，输入数据一开始就被分块存在集群磁盘里。

### 3.5Task Granularity

任务粒度指的是将map阶段划分为M个任务，将reduce阶段划分为R个任务的方式。作者指出，理想情况下，M和R应该比worker机器的数量大得多，这样可以提高动态负载均衡和故障恢复的效率。但是，M和R也不能太大，因为master需要做O(M+R)次调度决策，并且在内存中保持O(M\*R)的状态。另外，R通常受到用户的限制，因为每个reduce任务的输出都会保存在一个单独的输出文件中。作者给出了一个实际的例子，他们通常选择M使得每个任务的输入数据大小在16MB到64MB之间（这样可以最大化利用数据局部性优化），并且使R成为worker机器数量的一个小倍数。他们经常使用200000个map任务，5000个reduce任务，和2000台worker机器来进行MapReduce计算。

### 3.6Backup Tasks

备份任务是一种用来缓解拖延者问题的通用机制。拖延者指的是在计算过程中花费异常长时间来完成最后几个map或reduce任务的机器。备份任务的原理是，当一个MapReduce操作接近完成时，master会调度剩余的进行中的任务的备份执行。只要主执行或备份执行有一个完成，任务就被标记为完成。作者指出，这种机制可以显著减少大型MapReduce操作的完成时间，而只增加少量的计算资源消耗。作者给出了一个例子，当禁用备份任务机制时，排序程序的完成时间会增加44%。

