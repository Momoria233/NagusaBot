# NagusaBot

-   现有main分支历史遗留问题过多，已经暂时停止维护
-   从零开始重写，更新的-reform-版本仍在开发中，详见reform分支

## 现有功能

-   入群欢迎
-   吃饭功能
-   jm 下载（？）
-   还有不少 但是我还没写

## 部署方法

1. 安装 `pipx`

    > python -m pip install --user pipx  
    > python -m pipx ensurepath

    如果在此步骤的输出中出现了“open a new terminal”或者“re-login”字样，那么请关闭当前终端并重新打开一个新的终端。

2. 安装脚手架

    > pipx install nb-cli

    安装完成后，你可以在命令行使用 `nb` 命令来使用脚手架。如果出现无法找到命令的情况（例如出现“Command not found”字样），请参考 [pipx 文档](https://pypa.github.io/pipx/) 检查你的环境变量。

3. 克隆项目到本地

    > git clone https://github.com/Momoria233/NagusaBot.git  
    > cd NagusaBot

4. 配置 `.venv`

    > python3 -m venv .venv  
    > source .venv/bin/activate  
    > python -m pip install -r requirements.txt

5. 运行
    > nb run

## tbd

-   [ ] 接入数据库实现定时搬史
-   [x] ~~代码分类/优化可读性以及项目结构~~ 太难了 我只会写屎山
-   [x] 修复birthday插件
-   [x] 学生生日播报功能
-   [x] 根据特定群聊制定不同的welcome内容
-   [x] 完成naole.py
-   [x] 修复jm功能+制作白名单
-   [x] 拼好饭功能
-   [x] 拼好饭被偷功能
-   [x] 偷别人的拼好饭功能（已取消  因为不好玩
-   [x] 自动识别学生名字关键词同意入群（已取消 萝北说不用了
-   [x] 接入llm实现回复消息？（仅限whitelist中
-   [x] 接入llm实现群友语录查询并自动发送功能
-   [x] 通过 send_group_forward_msg 做“哎，大手”功能
-   [x] 通过 send_group_forward_msg 实现搬史 bot（？
-   [x] 关联夏莱烤肉屋自动转发
