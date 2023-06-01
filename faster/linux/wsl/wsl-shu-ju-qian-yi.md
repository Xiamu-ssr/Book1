---
description: 这是一个悲伤的故事。
---

# WSL数据迁移

### 复制虚拟磁盘

`C:\Users[user]\AppData\Local\Packages[distro]\LocalState\ext4.vhdx` 为 WSL2 磁盘所在位置，以 Microsoft 虚拟磁盘的形式存在。将其复制到我们的新机器上，在新机器上执行后续操作。

### 加载虚拟磁盘

HyperV 要求专业版、企业版、教育版 Windows。 先在 Windows 上启用 HyperV 组件，以管理员身份运行 Power Shell，执行以下指令：

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All 1
```

随后重启电脑即可完成 HyperV 的启用。再次以管理员身份运行 Power Shell，执行以下指令：

```powershell
Write-Output "\\.\PhysicalDrive$((Mount-VHD -Path <pathToVHD> -PassThru | Get-Disk).Number)"
```

记下其输出，如 `\\.\PhysicalDrive3`，此为虚拟磁盘在本机中的磁盘号&#x20;

### 将磁盘挂载至 WSL 中

在 Power Shell 中执行

```powershell
wsl --mount \\.\PHYSICALDRIVE3 --bare
```

### 在 WSL 中挂载磁盘

启动 WSL，创建挂载点，如 `/mnt/school` 文件夹

```bash
mkdir /mnt/school
```

以 root 用户的身份执行 `mount` 指令

```bash
mount /dev/sde /mnt/shool
```

{% hint style="info" %}
不知道是哪个dev，先在wsl下**`lsblk`**，然后powershell中**`wsl --unmount \\.\PHYSICALDRIVE3`**，再**`lsblk`**，看哪个消失了就是哪个。
{% endhint %}

即可挂载成功，可以通过 `ls` 查看

```bash
ls /mnt/school
```
