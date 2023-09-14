---
description: AbstractQueuedSynchronizer
---

# AQS

造成数据安全问题有以下三方面：

1.  可见性

    一个线程修改共享变量后，其他线程能立即看到这个修改

    可以使用volatile synchronized lock解决
2.  有序性

    编译器或者处理器指令重排序

    可以使用volatile synchronized lock解决
3.  原子性

    多个线程竞争同一数据
