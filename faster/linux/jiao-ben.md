---
description: auto run...pu..pu..pu
---

# 脚本

<details>

<summary>[0]向所有host发送文件或文件夹</summary>

```sh
#!/bin/bash
help="2 arguments:\n    first is PATH where scp from\n    second is PATH where scp to\n    first could both dir and file"

# 判断输入参数是否为2个
if [ $# -ne 2 ]; then
    echo -e $help
    exit 1
fi

# 获取输入参数
input=$1
output=$2

# 判断输入路径是否存在
if [ ! -e "$input" ]; then
    echo -e $help
    exit 1
fi

# 循环传输文件
for i in {0..4}; do
    host="hdp$i"
    # 判断输入路径是文件还是目录
    if [ -d "$input" ]; then
        scp -o StrictHostKeyChecking=no -r "$input" $host:"$output"
    else
        scp -o StrictHostKeyChecking=no "$input" $host:"$output"
    fi
done
```

</details>

<details>

<summary>[1]快速配置所有host免密</summary>

首先写一个one to all的免密脚本

```sh
# 判断输入路径是否存在
if [ ! -e $(echo ~/.ssh/id_rsa) ]; then
    ssh-keygen
else
    echo "find ~/.ssh/id_rsa"
fi

for i in {0..4}; do
    host="hdp$i"
    #sshpass明文跳过手动输入密码,关闭ssh-copy-id指纹验证
    sshpass -p "1009" ssh-copy-id -o StrictHostKeyChecking=no -i "$host"
done
```

然后用脚本\[0]把这个one to all传给所有节点。

在主节点再写一个脚本，循环让所有主机都执行一遍one to all，这就等于all to all了

```sh
for i in {0..4}; do
    host="hdp$i"
    sshpass -p "1009" ssh $host bash /home/mumu/Shell/ssh.sh
done
```

</details>
