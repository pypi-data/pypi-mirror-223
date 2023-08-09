# foyou-king
酷狗铃声搜索和下载

## 快速入门

[![python version](https://img.shields.io/pypi/pyversions/foyou-king)](https://pypi.org/project/foyou-king/)  [![Downloads](https://static.pepy.tech/personalized-badge/foyou-king?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/foyou-king)

安装

```shell
pip install -U foyou-king
```

> 关于库名：因为这属于偏向个人的库，为了尽可能不占用公共资源，所有库名看上去有些啰嗦。以后我开发的类似库，都会添加 **foyou-** 前缀。

安装完后会有两个命令行命令, `king` - 搜索铃声和 `yxiao` - 搜索音效

搜索铃声

```shell
# 默认显示 10 条铃声信息
king search love
```

下载铃声

```shell
# 默认下载 10 条铃声
king down love

# 搜索打嗝声音效
yxiao search 打嗝
```

## 搜索

```shell
king search <关键词> -p <页码-默认 1> -pn <分页大小-默认 10> 
```

## 搜索关键词提示

```shell
king tips <关键词> -pn <获取条数-默认 10>
```

## 下载

```shell
king down <关键词> -p <页码-默认 1> -pn <分页大小-默认 10> -n <铃声序号-多个可使用逗号连接>

# 例如要下载第 3 和第 5 条铃声
king down love -n 2,4
```

## 音效
> 搜索源来自站长之家

具体看命令行提示, 命令行命令是 `yxiao`
