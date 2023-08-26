# QA

<details>

<summary><code>docker exec id commad</code>执行命令时提示命令不存在，但是在容器中执行这个命令时却可以。</summary>

去`/usr/bin/`下创建软链接，因为docker exec应该默认只寻找部分路径的可执行文件。

</details>

<details>

<summary>docker update可以修改哪些属性</summary>

`docker update`命令用于更新正在运行的容器的配置。以下是您可以使用`docker update`命令修改的常见容器属性列表：

* `--cpu-shares`: 修改容器的 CPU 分配权重。
* `--memory`: 修改容器的内存限制。
* `--memory-swap`: 修改容器的交换空间限制。
* `--restart`: 修改容器的重启策略。
* `--network`: 修改容器的网络模式。
* `--cap-add`: 添加特权到容器。
* `--cap-drop`: 从容器中删除特权。
* `--volume`: 添加或删除容器的挂载卷。
* `--label-add`: 添加标签到容器。
* `--label-rm`: 从容器中删除标签。

请注意，`docker update`命令不能修改容器的基本配置，例如容器的镜像、命令或环境变量等。如果您需要修改这些配置，您需要停止并删除容器，然后使用新的配置重新启动容器。



</details>

<details>

<summary>--cap-add: 添加特权到容器。这个参数有哪些可选选项？都是什么意思</summary>

`--cap-add`选项用于向容器添加特权，特权可以让容器执行一些普通用户不能执行的操作。以下是`--cap-add`选项的一些常见特权选项及其作用：

* `ALL`: 添加所有特权。
* `AUDIT_CONTROL`: 允许容器启用和禁用审计功能。
* `AUDIT_WRITE`: 允许容器向审计日志写入记录。
* `CHOWN`: 允许容器更改任意文件的所有者。
* `DAC_OVERRIDE`: 允许容器忽略文件系统上的所有权限检查。
* `FOWNER`: 允许容器更改任意文件的所有者。
* `NET_ADMIN`: 允许容器执行网络管理任务，例如配置网络接口和 iptables 规则等。
* `NET_RAW`: 允许容器执行原始套接字操作，例如 ping 和 traceroute 等。
* `SETFCAP`: 允许容器设置文件系统功能。
* `SETUID`: 允许容器设置用户 ID。
* `SYS_ADMIN`: 允许容器执行系统管理任务，例如挂载文件系统和修改内核参数等。
* `SYS_CHROOT`: 允许容器使用 chroot() 调用。
* `SYS_PTRACE`: 允许容器使用 ptrace() 调用。
* `SYS_RESOURCE`: 允许容器修改系统资源限制。
* `SYS_TIME`: 允许容器更改系统时间。

请注意，在添加特权时，，一定要谨慎考虑安全风险，因为特权可以让容器执行一些危险的操作。如果您不确定需要哪些特权，请添加最小的特权集来限制容器的权限。

</details>

<details>

<summary>容器中删除文件后，大小不减反增怎么办？</summary>

Docker的镜像是由多层存储结构组成的，每一层都是只读的，所以您无法删除之前层的操作。

但是可以通过以下步骤达到一样的效果。

假设你从原始镜像a中创建了容器b。

现在你在容器b中删除了一些东西。

您可以使用docker export命令将容器的文件系统导出为一个tar文件:

```sh
docker export -o my.tar containerID
```

然后，使用docker import命令从这个tar文件导入为一个新的镜像:

```sh
docker import my.tar new-image
```

此时这个new-image镜像就摆脱了旧镜像的历史层，大小也会相应大大减少。



_但是你可能会失去一些东西：环境变量、端口映射、镜像的历史记录和层级结构、镜像的标签和版本号、镜像的创建时间和作者、容器的启动命令和参数等等。_

</details>
