---
description: 至少得知道，我们在做什么。
---

# 第一章-概

华为毕昇杯，目的是要写一个编译器，这个编译器要通过官方的一系列测试，官方用来测试的语言是[SySy](https://gitlab.eduxiji.net/nscscc/compiler2022/-/blob/master/SysY2022%E8%AF%AD%E8%A8%80%E5%AE%9A%E4%B9%89-V1.pdf)，一门简小版的C语言。你的编译器不仅要编译成功SySy文件，而且得到的可执行文件运行时要又准又快。

{% embed url="https://gitlab.eduxiji.net/nscscc/compiler2022/-/blob/master/SysY2022%E8%AF%AD%E8%A8%80%E5%AE%9A%E4%B9%89-V1.pdf" %}

编译器是如何工作的？

从C语言中，我们可以了解到，从一个.c文件到一个可执行文件，大抵可以分为以下三个阶段

1. 编译
2. 汇编
3. 链接

我们的大部分工作，将被规划在第一点，单从这一点看，编译器通常分为以下三个部分

1. 前端：词法分析、语法分析-得到抽象语法树（ATS，abstract syntax tree）、语义分析、中间代码生成-得到中间表示（IR，intermediate representation）
2. 中端：优化、分析、变化
3. 后端：指令选择、寄存器分配、指令调度、代码生成-得到可执行二进制文件

每个字都认识，加在一起，就不明白是什么意思了。

之后的章节将介绍细节，到时自然会明白。
