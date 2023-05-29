# Page 2

`docker exec id commad`执行命令时提示命令不存在，但是在容器中执行这个命令时却可以。

去`/usr/bin/`下创建软链接，因为docker exec应该默认只寻找部分路径的可执行文件。
