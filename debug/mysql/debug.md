# DeBug

## mysqld: File './binlog.index' not found (OS errno 13 - Permission denied)

`chown -R mysql:mysql /var/lib/mysql`把mysql文件夹归到mysql用户和用户组下，路径表示mysql安装路径，可能不一样。
