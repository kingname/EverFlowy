# 从Workflowy到印象笔记


Workflowy是一个极简风格的大纲写作工具，使用它提供的无限层级缩进和各种快捷键，可以非常方便的理清思路，写出一个好看而实用的大纲。如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-10-17-58.png)

印象笔记更是家喻户晓，无人不知的跨平台笔记应用。虽然有很多竞争产品在和印象笔记争抢市场，但是印象笔记强大的搜索功能还是牢牢抓住了不少用户。

如果能够把用Workflowy写大纲的便利性，与印象笔记强大的搜索功能结合起来，那岂不是如虎添翼？如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-10-21-31.png)

EverFlowy就是这样一个小工具。它可以自动把Workflowy上面的条目拉下来再同步到印象笔记中。如果Workflowy有更新，再运行一下这个小工具，它就会同步更新印象笔记上面的内容。Workflowy负责写，印象笔记负责存，各尽其能，各得其所。

<!--more-->

## 工具介绍
Everflowy基于Python 3开发，代码托管在Github中，地址为：[https://github.com/kingname/EverFlowy](https://github.com/kingname/EverFlowy)这个小工具在持续开发中，目前可以实现Workflowy单向同步到印象笔记和差异更新。由于印象笔记的Oauth验证方式需要申请才能对正式的账号使用，但它又不会通过这种个人小工具的申请，所以目前暂时使用开发者Token。关于如何申请开通正式账号的开发者Token，在后文会有详细的说明。

## 安装
首先需要保证电脑中安装了Python 3，否则无法运行这个小工具。代码的依赖关系使用Pipenv来管理，所以需要首先使用pip安装pipenv：

```bash
python3 -m pip install pipenv
```

有了Pipenv以后，使用Git把代码拉到本地再安装依赖：

```bash
git clone https://github.com/kingname/EverFlowy.git
cd EverFlowy
pipenv install
pipenv shell
```

运行了上面的4条命令以后，你的终端窗口应该如下图类似。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-10-43-11.png)

Pipenv会自动创建一个基于Virtualenv的虚拟环境，然后把EverFlowy依赖的第三方库自动安装到这个虚拟环境中，再自动激活这个虚拟环境。

## 配置
在代码的根目录，有一个config.json文件，打开以后如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-10-46-26.png)

你需要修改三个地方，分别是`username`，`password`和`dev_token`。其中`username`和`password`分别对应了Workflowy的用户名和密码，而`dev_token`是印象笔记的开发者Token。

这里需要说明一下印象笔记的开发者Token。印象笔记的开发者Token有两套，分别是沙盒环境的开发者Token和生产环境的开发者Token。所谓沙盒环境，就是一个测试开发环境，这个环境是专门为了快速开发印象笔记App而设计的，它的地址为：[https://sandbox.evernote.com](https://sandbox.evernote.com)。打开这个网址，可以看到页面上弹出了警告，如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-10-56-01.png)

无论你之前是否有印象笔记的账号，要使用沙盒环境，都必需重新注册。注册完成以后，通过访问[https://sandbox.evernote.com/api/DeveloperToken.action](https://sandbox.evernote.com/api/DeveloperToken.action)获取沙盒环境的开发者Token。

关于印象笔记的沙盒环境，我将另外开一篇文章来说明。本文主要介绍如何申请生产环境的开发者Token，从而可以使用正式的印象笔记账号。

在2017年6月以后，印象笔记关闭了生产环境开发者Token的申请通道，如果打开申请网址：[https://app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action)，你会发现申请的按钮是灰色的且无法点击。要解决这个问题，就需要让印象笔记的客服帮忙。

登录自己的印象笔记正式账号，打开印象笔记首页，把页面拉到最下面，可以看到有一个“联系我们”，如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-11-13-41.png)

进入“联系我们”，点击“联系客服”，如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-11-14-06.png)

在联系客服的页面填写如下信息，最后一项“简要描述问题”填写“我需要基于印象笔记API开发，请帮我开通生产环境开发者Token”并提交。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-11-17-01.png)

大约24小时内，就可以受到客服回复的邮件，如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-11-19-02.png)

此时再次打开[https://app.yinxiang.com/api/DeveloperToken.action](https://app.yinxiang.com/api/DeveloperToken.action)就可以申请开发者Token了，如下图所示。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2018-03-17-11-20-23.png)

需要注意的是，开发者Token只会显示一次，所以你需要立刻把它记录下来。

## 运行

有了生产环境的开发者Token以后，把它填写到config.json中，配置就算完成了。在终端输入命令：

```bash
python3 EverFlowy.py
```

程序就可以开始同步Workflowy的数据到印象笔记了。

同步完成以后，你会发现程序的根目录出现了一个history.db文件。这是一个sqllite的文件，里面就是你在Workflowy中的所有大纲内容和对应的印象笔记GUID和enml格式的内容。这是为了实现数据的差异更新而生成的。你可以使用各种能够浏览sqllite的工具来查看里面的内容。

## 已知问题

* 如果删除了history.db，那么再次运行Everflowy，Workflowy中的所有内容都会再次写入印象笔记。
* 如果单独删除了EverFlowy写入印象笔记中的某一条目，却不删除history.db中的对应条目，WorkFlowy会因为找不到GUID而抛出异常。
* 没有测试国际版印象笔记账号是否可用。
* 如过你想测试沙盒环境的开发者账号，请修改`evernote_util/EverNoteUtil.py`第98行，把

```python
client = EvernoteClient(token=self.dev_token, sandbox=False, service_host='app.yinxiang.com')
```

修改为：

```python
client = EvernoteClient(token=self.dev_token)
```

