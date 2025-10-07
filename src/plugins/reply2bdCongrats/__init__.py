import time

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, GroupMessageEvent


bd_handle = on_regex(pattern=r"生日快乐",priority=1)
@bd_handle.handle()
async def bd_reply(bot: Bot, event: GroupMessageEvent):
    now = time.localtime()
    if (now.tm_mon == 12 and now.tm_mday == 7) == False:
        await bd_handle.finish()
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    self_id = event.self_id  
    if any(seg.type == "at" and seg.data.get("qq") == self_id for seg in event.message)==True:
        await bd_handle.finish(message=Message([at," 谢谢老师！"]))
    else:
        await bd_handle.finish()