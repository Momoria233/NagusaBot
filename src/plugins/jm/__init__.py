from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.rule import to_me

from .config import Config
from .jmdownload import jm_download, jm_init

driver = get_driver()


@driver.on_startup
async def init_func():
    logger.info("loading config...")
    jm_init()
    logger.info("config loaded")


jmDown = on_command("jm", rule=to_me(), priority=1, block=True)


@jmDown.handle()
async def download_func(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if not event.group_id in Config.group_whitelist:
        jmDown.skip()
        return
    reply = MessageSegment.reply(event.message_id)
    at = MessageSegment.at(event.get_user_id())
    if number := args.extract_plain_text():
        logger.info(f"downloading jmcode {number}")
        code, msg = await jm_download(number)
        if code != 0:
            text = MessageSegment.text(" " + msg)
            await jmDown.finish(message=Message([reply, at, text]))
        await bot.call_api("upload_group_file", group_id=event.group_id, file=msg, name=f"{number}.pdf")
        msg = "下载成功"
        text = MessageSegment.text(" " + msg)
        await jmDown.finish(message=Message([reply, at, text]))

    else:
        msg = "请输入车牌号"
        text = MessageSegment.text(" " + msg)
        await jmDown.finish(message=Message([reply, at, text]))

jmPriv = on_command("jm", rule=to_me(), priority=1, block=True)
@jmPriv.handle()
async def download_func(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    if not Config.allow_private or event.get_user_id() not in Config.user_whitelist:
        jmPriv.skip()
        return
    reply = MessageSegment.reply(event.message_id)
    at = MessageSegment.at(event.get_user_id())
    if number := args.extract_plain_text():
        logger.info(f"downloading jmcode {number}")
        code, msg = await jm_download(number)
        if code != 0:
            text = MessageSegment.text(" " + msg)
            await jmPriv.finish(message=Message([reply, at, text]))
        await bot.call_api("upload_private_file", user_id=event.get_user_id(), file=msg, name=f"{number}.pdf")
        msg = "下载成功"
        text = MessageSegment.text(" " + msg)
        await jmPriv.finish(message=Message([reply, at, text]))

    else:
        msg = "请输入车牌号"
        text = MessageSegment.text(" " + msg)
        await jmPriv.finish(message=Message([reply, at, text]))
