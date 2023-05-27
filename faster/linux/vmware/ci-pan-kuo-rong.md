# 磁盘扩容

关机后进入设置，扩容磁盘。开机。

`fdisk /dev/nvme0n1`进入/nvme0n1磁盘操作命令行，`n`新建分区，设置分区序号和首尾位置。`w`保存，`q`退出。

`fdisk -l`和`lsblk`查看磁盘和分区和逻辑卷情况

`echo 1 > /sys/class/nvme/nvme0/device/rescan`和`partprobe /dev/nvme0n1`通知内核重新读取分区表，以便更新分区信息。

`pvcreate /dev/nvme0n1p3`在/dev/nvme0n1p3分区创建一个物理卷，`pvdisplay`可以查看所有物理卷信息。

`vgextend centos /dev/nvme0n1p3`把新的物理卷加入到centos卷组(VG)中，vgdisplay查看VG信息。

`lvextend -l +100%FREE /dev/centos/root`把VG的所有剩余空间给root逻辑卷(LV)，`lvdisplay`查看LV信息。

`xfs_growfs /dev/mapper/centos-root`调整XFS文件系统大小，`df -lh`查看是否已扩容。
