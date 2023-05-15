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
编译器检查这棵 AST 是否有意义，并记录符号表：

```
Symbol Table:
    main: Function, Type: int, Parameters: (), Scope: Global
    x: Variable, Type: int, Scope: main

Semantic Errors:
    None
```

~~我没看懂这个符号表~~
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

以下是new bing给出的一份main函数样例

```cpp
#include <iostream>
#include <fstream>
#include <sstream>

#include "TLLexer.h"
#include "TLParser.h"
#include "TLVisitor.h"
#include "tree/ParseTreeVisitor.h"

std::string read_file(const std::string& filename) {
    std::ifstream infile(filename);
    std::stringstream buffer;
    buffer << infile.rdbuf();
    std::string file_content = buffer.str();
    infile.close();
    return file_content;
}

int main(int argc, const char* argv[]) {
  //输入文件名，读取文件内容
  std::string file_content = read_file(argv[1]);
  //载入到antlr4输入流
  antlr4::ANTLRInputStream input(file_content);
  //用input作为参数构建TLLexer类，名为lexer
  TLLexer lexer(&input);
  //用lexer作为参数构建token流
  antlr4::CommonTokenStream tokens(&lexer);
  //用token流构建TLParser类，名为parser，至此已完成词法分析和语法分析
  TLParser parser(&tokens);
  return 0;
}

```
{% endtab %}

{% tab title="语义分析" %}
修改visitor类，在visitor遍历查看AST时，添加你的自定义操作，完成AST的纠错和优化。

并在main中继续添加

<pre class="language-cpp"><code class="lang-cpp"><strong>  //从parser获取到AST
</strong>  antlr4::tree::ParseTree* tree = parser.parse();
  //使用visitor去检查这棵AST，如果你修改了visitor代码，那么至此已完成语义分析
  TLVisitor visitor;
  visitor.visit(tree);
</code></pre>
{% endtab %}
{% endtabs %}
