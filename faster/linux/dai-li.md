---
description: 我之所以看的更远，是因为我站在梯子上。
---

# 代理

{% embed url="https://github.com/vpncn/vpncn.github.io" %}

## 机场

{% tabs %}
{% tab title="樱花机场" %}
{% embed url="https://dy.ssrla.de/auth/register?code=VXwq" %}

均衡的樱花机场。

价格也很便宜，但是最近几个月，稳定性开始变差。
{% endtab %}

{% tab title="两元店" %}
{% embed url="https://xn--5hqx9equq.com/#/register?code=9hHIaNoU" %}

听说是一个把性价比练到三星五费的机场
{% endtab %}

{% tab title="一元店" %}
{% embed url="https://xn--4gq62f52gdss.com/#/register?code=chfOv0bl" %}

性价比也是史诗的存在
{% endtab %}
{% endtabs %}

## 使用

{% tabs %}
{% tab title="Windows" %}
用clash，简便高效，顺便把v2ray也带上

{% embed url="https://github.com/Fndroid/clash_for_windows_pkg" %}

{% embed url="https://github.com/v2fly/v2ray-core" %}
{% endtab %}

{% tab title="Linux" %}
相信我，无GUI，不要用clash，再把proxychains4带上。

{% embed url="https://github.com/v2fly/v2ray-core" %}

{% embed url="https://github.com/rofl0r/proxychains-ng" %}

`./configure --prefix=/usr --sysconfdir=/etc && make -j && make install` 从源码编译安装proxychains4

{% hint style="info" %}
安装后没有proxychains4.conf文件，手动touch，填入以下内容

```tsconfig
strict_chain
proxy_dns 
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
http    127.0.0.1 7891
socks5  127.0.0.1 7890
```
{% endhint %}

{% hint style="info" %}
没有sudo权限，可以选择安装在自己目录下，并在`~/.bashrc`之类的文件中添加以下代码

```sh
export PROXYCHAINS_CONF_FILE=/home/mokanglong/etc/proxychains4.conf
export PATH=/home/mokanglong/usr/bin:$PATH
```
{% endhint %}
{% endtab %}
{% endtabs %}



