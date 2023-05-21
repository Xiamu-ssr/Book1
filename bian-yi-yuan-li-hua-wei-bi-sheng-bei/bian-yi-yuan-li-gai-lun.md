---
description: 至少得知道，我们在做什么。
---

# 第一章-概

编译原理是一门研究如何把一种编程语言转换成另一种编程语言的学科。一种常见的转换是把高级语言（比如C++或Java）转换成低级语言（比如汇编或机器码），这样就可以在计算机上执行。这种转换的过程叫做编译，而执行这种转换的程序叫做编译器。

华为毕昇杯，目的是要写一个编译器，这个编译器要通过官方的一系列测试，官方用来测试的语言是[SySy](https://gitlab.eduxiji.net/nscscc/compiler2022/-/blob/master/SysY2022%E8%AF%AD%E8%A8%80%E5%AE%9A%E4%B9%89-V1.pdf)，一门简小版的C语言。你的编译器不仅要编译成功SySy文件，而且得到的可执行文件运行时要又准又快。[https://gitlab.eduxiji.net/nscscc/compiler2023/-/tree/master](https://gitlab.eduxiji.net/nscscc/compiler2023/-/tree/master)

{% embed url="https://gitlab.eduxiji.net/nscscc/compiler2023/-/tree/master" %}
SySy语言定义
{% endembed %}

一个编译器通常分为两个部分：前端和后端。

前端负责分析输入的源代码，理解它的结构和含义，并生成一个中间表示，比如抽象语法树（AST）。

后端负责根据中间表示，生成目标代码，比如汇编或机器码。

1. 前端：词法分析、语法分析-得到抽象语法树（ATS，abstract syntax tree）、语义分析、中间代码生成-得到中间表示（IR，intermediate representation）
2. 后端：优化、生成目标代码

每个字都认识，加在一起，就不明白是什么意思了。

之后的章节将介绍细节，到时自然会明白。
