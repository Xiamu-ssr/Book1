# 安装专业安装工具Ambari

{% embed url="https://cwiki.apache.org/confluence/display/AMBARI/Installation+Guide+for+Ambari+2.7.7" %}

## 安装依赖

```sh
sudo apt update && sudo apt install openjdk-8-jdk maven
```

## Build and install Ambari <a href="#installationguideforambari2.7.7-buildandinstallambari2.7.7" id="installationguideforambari2.7.7-buildandinstallambari2.7.7"></a>

下载，解压，编译

```sh
wget https://www-eu.apache.org/dist/ambari/ambari-2.7.7/apache-ambari-2.7.7-src.tar.gz
tar xfvz apache-ambari-2.7.7-src.tar.gz
cd apache-ambari-2.7.7-src
mvn versions:set -DnewVersion=2.7.7.0.0
#long time has passed......
pushd ambari-metrics
mvn versions:set -DnewVersion=2.7.7.0.0
popd
```

清理，编译，打包，安装

```sh
mvn -B clean install jdeb:jdeb -DnewVersion=2.7.7.0.0 -DbuildNumber=388e072381e71c7755673b7743531c03a4d61be8 -DskipTests -Dpython.ver="python >= 2.6"
```
