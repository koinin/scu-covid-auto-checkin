# **四川大学健康每日报自动打卡工作流**

![auto-checkin](https://github.com/hx-w/scu-covid-auto-checkin/workflows/auto-checkin/badge.svg)
![collage](https://img.shields.io/badge/collage-SCU-ff69b4)

本项目力在提供一种对SCU学生每日健康打卡顺利完成的**最后保障**，项目中定时打卡的功能使用GitHub Action实现，不需要自备服务器资源。

在使用该项目之前你需要了解相关的风险。

我只列举其中一条：一旦发现本项目有被滥用的情况，开发者随时准备删库跑路。

打卡脚本的实现原理见：[对SCU网络服务安全性的第一次探索](https://blog.hx-w.top/article/a44f/)

## 快速开始

1. **fork**本项目，接下来的操作都在你fork后的仓库里操作
2. 添加环境变量`EAI_SESS`、`UUKEY`和`CAMPUS`
3. 更改配置文件中的定时信息`.github/workflows/auto-checkin.yml`

具体操作见：[**详细流程**](#详细流程)

## 详细流程

### 获取关键变量

1. 用**Chrome**或**Edge**浏览器打开[四川大学微服务-健康每日报](https://wfw.scu.edu.cn/ncov/wap/default/index)

2. 按F12，打开开发者工具，选中右侧上方的**Network** 
    ![切换至Network](https://ibed.csgowiki.top/image/fig-1.png)

3. 刷新页面，在Network选项卡中下方Name中找到**index**，在右侧**Headers**下方找到**Cookie**项，复制出其中的`eai_sess`与`UUkey`内容备用
    ![找到cookies](https://ibed.csgowiki.top/image/find-cookies.png)

    > 注意：cookie中`eai_sess`与`UUkey`的表示方式为`eai_sess=1234; UUkey=5678;`，只需要获取`=`与`;`之间的字符即可，即`1234`与`5678`。
    >
    > ** 理论上 泄漏`eai_sess`与`UUkey`意味着泄漏你的打卡权限，请妥善保存这些敏感数据。 **

### 添加环境变量

获取了`eai_sess`与`UUkey`之后，就可以在你fork后的github仓库中添加环境变量，以便打卡脚本的运行。

1. **在你fork后的仓库里** 进入Settings -> Secrets，点击右上角的**New repository secret**

    ![找到Secrets](https://ibed.csgowiki.top/image/add_secrets.png)

2. 一共添加3个环境变量：
    | Name | Value |
    | ---- | ---- |
    | `EAI_SESS` | 获取的`eai_sess` |
    | `UUKEY` | 获取的`UUkey` |
    | `CAMPUS` | 所在校区，填`wangjiang`、`jiangan`或`huaxi` |

> 现在还未提供`jiangan(江安)`与`huaxi(华西)`的地理位置模板
### 修改定时配置

修改`.github/workflows/auto-checkin.yml`

更改`cron`配置，参考：[wiki](https://zh.wikipedia.org/wiki/Cron)

默认的配置是：每天早上8点左右执行脚本

**注意** 执行的时间是UTC时间，北京时间需要在cron对应的小时上再+8 ，所以`0 0 * * *`代表了在每天UTC时间0点0分时触发事件，即每天北京时间8点触发。

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'
```