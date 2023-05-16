---
description: 虽然都叫前端，但我明显比web前端更难懂。
---

# 第二章-前端

你好，这是Bing。我很高兴你想要了解更多关于编译器前端的细节。😊

为了让你更容易理解，我为你准备了一个简单的例子，来展示编译器前端的三个部分是如何工作的。

假设我们有一个源代码文件，名为example.c，内容如下：

```c
// This is a comment
int main() {
    int x = 1 + 2;
    return x;
}
```

{% tabs %}
{% tab title="词法分析" %}
编译器前端会读取这个文件的内容，并将它分割成一个个的单词（token）。单词是源代码中最小的有意义的单位，它们可以是标识符，关键字，常量，运算符等。在这个过程中，编译器前端会忽略空白和注释，因为它们对于源代码的意义没有影响。经过词法分析后，我们得到以下单词序列：

```
int
main
(
)
{
int
x
=
1
+
2
;
return
x
;
}

```


{% endtab %}

{% tab title="语法分析" %}
编译器前端会根据语言的语法规则，将单词序列组合成一个个的语句，并检查它们是否符合语法规则。语句是源代码中具有完整含义的单位，它们可以是表达式，赋值语句，控制流语句等。在这个过程中，编译器前端会构建出一个抽象语法树（AST），来表示源代码的结构和逻辑。抽象语法树是一种树形的数据结构，每个节点都代表了一个语句或者一个操作。例如，第三行的`int x = 1 + 2;`就可以表示为以下的抽象语法树：

```
    DeclarationStatement
    /        |         \
Type      Name     Initializer
 |         |           |
int        x     BinaryExpression
                  /      |      \
             Operator LeftOperand RightOperand
                |        |          |
                +        1          2
 
```
{% endtab %}

{% tab title="语义分析" %}
编译器的语义分析阶段是编译过程中的重要阶段之一，主要负责对源代码进行语义分析，检查程序中是否存在语义错误，并在必要时进行纠正。下面是一些编译器在语义分析阶段通常会进行的检查和纠正：

1. 变量和函数的声明和定义检查：编译器会检查变量和函数的声明和定义是否匹配，例如检查变量的类型是否与其声明时的类型一致，检查函数的参数类型和个数是否匹配等。
2. 变量和函数的作用域检查：编译器会检查变量和函数的作用域是否正确，例如检查变量是否在其作用域范围内被使用，检查函数是否在其可见的作用域内被调用等。
3. 类型检查和转换：编译器会检查表达式的类型是否正确，例如检查赋值语句左右两侧的类型是否一致，检查条件表达式的类型是否为布尔型等。如果类型不一致，编译器会尝试进行隐式类型转换或报错。
4. 数组和指针检查：编译器会检查数组和指针的使用是否正确，例如检查数组下标是否越界，检查指针是否为NULL等。
5. 控制流检查：编译器会检查程序中的控制流是否正确，例如检查循环语句中是否存在死循环，检查条件语句中是否存在无法到达的分支等。
6. 常量表达式计算：编译器会对常量表达式进行计算，例如检查数组大小是否为常量表达式，检查枚举类型是否为常量表达式等。
7. 错误纠正：如果编译器在语义分析阶段发现了错误，它会尝试进行纠正，以便继续进行后续的编译工作。例如，编译器可能会在变量未声明时尝试在当前作用域中查找该变量的声明，或者在函数调用时尝试在可见的作用域中查找函数的定义。

需要注意的是，不同的编程语言和编译器可能会进行不同的语义分析检查和纠正。上述列表只是一些常见的检查和纠正，具体实现可能会根据编程语言和编译器的不同而有所差异。
{% endtab %}

{% tab title="中间代码生成" %}

{% endtab %}
{% endtabs %}

也许看明白了，但是怎么实操呢？

首先你得懂扩展巴科斯范式（EBNF，Extended Backus–Naur Form）和[antlr4](https://github.com/antlr/antlr4)

ANTLR4是一个工具，可以帮助你快速地构建编译器的前端部分。你只需要用一种特殊的语法来描述你的编程语言的规则，然后ANTLR4就可以根据这些规则，生成一个词法分析器和一个语法分析器。

ANTLR4还可以让你自定义一个访问者（visitor），这是一个类，可以遍历解析树中的每个节点，并对每个节点执行一些操作。你可以在访问者中实现你自己的逻辑，比如生成AST、检查错误、执行代码等。

{% embed url="https://github.com/antlr/antlr4" %}

{% embed url="https://www.antlr.org/api/Java/index.html" %}

{% tabs %}
{% tab title="词法分析和语法分析" %}
首席配置好antlr4环境并下载好antlr4的runtime

根据SySy语言的定义，写一份g4文件，大抵像这样：

```
grammar SysY;

program     : (decl ';' | funcdef)+ EOF
            ;

expr        : addexpr
            ;

。。。
            
VOID    : 'void';
FLOAT   : 'float';
INT     : 'int';
IF      : 'if';
ELSE    : 'else';
```

然后使用命令`antlr4 -visitor -Dlanguage=Cpp SysY.g4`生成出许多cpp文件和h文件，然后这些文件里的类或者方法什么的，就都可以直接调用了。

接下来就可以写main函数了，这个main函数可以调用runtime，也可以调用上面所说生成的cpp，然后使用c++编译器编译这个main函数，得到一个可执行文件，这个可执行文件就是我们的SySy编译器。很神奇是不是，都快自举了。但是这个main函数不是一下就能写完的，比如我们目前只完成了词法分析和语法分析，main函数最后可能只能输出抽象语法树AST，离真正的编译器还差些距离。

以下是GPT给出的一份main函数样例

```cpp
#include <iostream>
#include "antlr4-runtime.h"
#include "MyLexer.h"
#include "MyParser.h"
#include "MyVisitor.h"

using namespace antlr4;

int main(int argc, const char* argv[]) {
    std::ifstream stream;
    stream.open(argv[1]);
    ANTLRInputStream input(stream);
    MyLexer lexer(&input);
    CommonTokenStream tokens(&lexer);
    MyParser parser(&tokens);
    tree::ParseTree* tree = parser.program();
    MyVisitor visitor;
    visitor.visit(tree);
    return 0;
}
```

这个 main 函数做了以下几件事情：

1. 打开输入文件并将其转换为 ANTLRInputStream。
2. 使用 MyLexer 将输入流转换为token流。
3. 使用 MyParser 将标记流转换为AST。
4. 创建 MyVisitor 的实例并使用它来遍历语法树。

这个示例仅是一个基本的模板，你需要根据你的语言和编译器的需求进行修改。在这个示例中，MyLexer、MyParser 和 MyVisitor 都是从你的 ANTLR 4 语法文件生成的 C++ 类。
{% endtab %}

{% tab title="语义分析" %}
如果你已经修改了visitor类，在visitor遍历查看AST时，你的自定义操作，能够完成AST的纠错和优化，那么前面写的这三行代码，已经完成了语义分析。

```cpp
    tree::ParseTree* tree = parser.program();
    MyVisitor visitor;
    visitor.visit(tree);
```

在这个阶段，我们选择通过符号表的方式，完成对整棵AST的检查和纠错。


{% endtab %}
{% endtabs %}
