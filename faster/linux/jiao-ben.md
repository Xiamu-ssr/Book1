---
description: auto run...pu..pu..pu
---

# 脚本

<details>

<summary>[0]快速向所有host发送文件或文件夹</summary>

_<mark style="color:red;">需保证所有.sh在\~/Shell文件夹下</mark>_

首先需要一个记录config的sh

```sh
#config.sh
hosts=(
hdp0
hdp1
hdp2
)
passwd="1009"
```

然后写一个明文传输密码的scp.sh

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

source $(echo ~/Shell)/config.sh
# 循环传输文件
for host in "${hosts[@]}"; do
    # 判断输入路径是文件还是目录
    if [ -d "$input" ]; then
        sshpass -p $passwd scp -o StrictHostKeyChecking=no -r "$input" $host:"$output"
    else
        sshpass -p $passwd scp -o StrictHostKeyChecking=no "$input" $host:"$output"
    fi
done
```

`bash scp.sh /root/Shell /root`即可将本地Shell文件夹或Shell文件传输到所有$hosts

</details>

<details>

<summary>[1]快速配置所有host免密</summary>

_<mark style="color:red;">需保证所有.sh在\~/Shell文件夹下</mark>_

首先需要一个记录config的sh

```sh
#config.sh
hosts=(
hdp0
hdp1
hdp2
)
passwd="1009"
```

然后写one\_to\_all的免密

```sh
source $(echo ~/Shell)/config.sh
# 判断输入路径是否存在
if [ ! -e $(echo ~/.ssh/id_rsa) ]; then
    ssh-keygen -t rsa -N "" -f $(echo ~/.ssh/id_rsa)
else
    echo "find "$(echo ~/.ssh/id_rsa)
fi

for host in "${hosts[@]}"; do
    #sshpass明文跳过手动输入密码,关闭ssh-copy-id指纹验证
    sshpass -p $passwd ssh-copy-id -o StrictHostKeyChecking=no -i "$host"
done
```

然后用脚本\[0]把这个one to all传给所有节点。

在主节点再写一个脚本，循环让所有主机都执行一遍one to all，这就等于all to all了

```sh
source $(echo ~/Shell)/config.sh
for host in "${hosts[@]}";do
    sshpass -p $passwd ssh $host 'bash -s' < $(echo ~/Shell)/ssh_one_to_all.sh
done
```

`bash all_to_all.sh`即可自动配置$hosts之间的互相免密

</details>

