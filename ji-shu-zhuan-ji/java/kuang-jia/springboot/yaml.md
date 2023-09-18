# YAML

## 数据格式

对象

```yaml
person:
    name: zhangsan
# 或者
person: {name: zhangsan}
```

数组

```yaml
address:
    - beijing
    - shanghai
#or
address: [beijing, shanghai]
```

常量

```yaml
msg1: 'hello \n world'#单引号忽略转义字符
msg2: "hello \n world"#双引号识别转义字符
```
