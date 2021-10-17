# **四川大学健康每日报自动打卡工作流**(scu-covid-auto-checkin)

![auto-checkin](https://github.com/hx-w/scu-covid-auto-checkin/workflows/auto-checkin/badge.svg)
![collage](https://img.shields.io/badge/collage-SCU-ff69b4)

## 快速开始

1. **fork**本项目，接下来的操作都在你fork后的仓库里操作
2. 添加环境变量`EAI_SESS`、`UUKEY`和`CAMPUS`
3. 更改配置文件中的定时信息`.github/workflows/autocheckin.yml`

具体操作见：[**详细流程**](#详细流程)

## 详细流程

### 获取关键变量

1. 用**Chrome**或**Edge**浏览器打开[四川大学微服务-健康每日报](https://wfw.scu.edu.cn/ncov/wap/default/index)

2. 按F12，打开开发者工具，选中右侧上方的**Network** 
    ![切换至Network](https://ibed.csgowiki.top/image/fig-1.png)

3. 刷新页面，在Network选项卡中下方name中找到**index**，在右侧**Headers**下方找到**Cookie**项，复制出其中的`eai_sess`与`UUkey`内容备用
    ![找到cookies](https://ibed.csgowiki.top/image/find-cookies.png)

    > 注意：cookie中`eai_sess`与`UUkey`的表示方式为`eai_sess=1234; UUkey=5678;`，只需要获取`=`与`;`之间的字符即可，即`1234`与`5678`。
    > **理论上 泄漏`eai_sess`与`UUkey`意味着泄漏你的打卡权限，请妥善保存这些敏感数据。

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

### 修改定时配置


