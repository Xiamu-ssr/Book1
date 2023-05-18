# 第二章-面向公众的前后端

## 框架配置

|        |                                 |
| ------ | ------------------------------- |
| 前端基础框架 | Vue3(typescript+SFC+组合式API)     |
| 前端样式框架 | Element-plus+Bootstrap5+ECharts |
| 后端响应框架 | Flask                           |

{% embed url="https://cn.vuejs.org/" %}
Vue3
{% endembed %}

{% embed url="https://element-plus.gitee.io/zh-CN/" %}
element-plus
{% endembed %}

{% embed url="https://v5.bootcss.com/" %}
bootstrap5
{% endembed %}

{% embed url="https://vue-echarts.dev/" %}
vue echarts
{% endembed %}

{% embed url="https://flask.palletsprojects.com/en/2.3.x/" %}
flask
{% endembed %}

## 文件描述

/src下有以下文件夹和文件

* App.vue
* assets
* components
* main.ts：vue配置文件
* router
* views

{% tabs %}
{% tab title="App.vue" %}
vue框架构建Web项目运行入口文件。
{% endtab %}

{% tab title="assets" %}
存放图片等资源文件夹。存放vue文件
{% endtab %}

{% tab title="components" %}
组件文件夹。拥有以下文件

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th></tr></thead><tbody><tr><td>Index_search.vue</td><td>主页搜索组件</td></tr><tr><td>Species_list.vue</td><td>物种名录组件</td></tr><tr><td>Protected_species_list.vue</td><td>保护物种名录组件</td></tr><tr><td>National_park_species_list.vue</td><td>国家公园物种名录组件</td></tr><tr><td>show_data.vue</td><td>数据展示组件</td></tr><tr><td>search.py</td><td>后端响应程序</td></tr></tbody></table>
{% endtab %}

{% tab title="router" %}
index.ts路由配置文件
{% endtab %}

{% tab title="views" %}
视图文件夹。包括以下文件

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td>index.vue</td><td>网站主页视图</td><td></td></tr><tr><td>show_data.vue</td><td>数据展示视图</td><td></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

<img src="../.gitbook/assets/file.excalidraw.svg" alt="" class="gitbook-drawing">
