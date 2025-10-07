import os
import random
import time
from datetime import datetime

import nonebot
from nonebot import logger, on_notice, on_regex, on_command, on_message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    LuckyKingNotifyEvent,
    Message,
    MessageSegment,
    PokeNotifyEvent,
)
from nonebot.typing import T_State
from nonebot.params import CommandArg
from .llmResp import get_yulu_response, get_yulu_reason
from .config import Config
from .llmCensor import *
import re

assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

cooldown_tracker = {}
cooldown_period = Config.cooldown_period

MAX_HISTORY = 50

group_message_history: dict[int, list[str]] = {}

# def fetchRecentMsg(group_id: int, count: int = 5) -> list[str]:
#     messages = group_message_history.get(group_id, [])
#     return messages[-count:] if messages else []

# record_message = on_message(priority=99, block=False)

# @record_message.handle()
# async def record_message_handle(event: GroupMessageEvent):
#     group_id = event.group_id
#     message = str(event.get_message())

#     if "[CQ:image" in message or "[CQ:mface" in message or "[CQ:record" in message:
#         return

#     match = re.search(r']\s*(.+)', message)
#     if match:
#         message = match.group(1).strip()

#     if group_id not in group_message_history:
#         group_message_history[group_id] = []

#     group_message_history[group_id].append(message)

#     if len(group_message_history[group_id]) > MAX_HISTORY:
#         group_message_history[group_id].pop(0)

# revL = on_command("rev",priority=5, block=True)

# @revL.handle()
# async def rev(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
#     group_id = event.group_id
#     # if not event.user_id in Config.usr_whitelist:
#     #     await matcher.finish()

#     try:
#         n = int(str(args).strip()) if str(args).strip() else 5
#     except ValueError:
#         await matcher.finish(message=Message("格式错误，请输入 /rev [数字]"))

#     last_messages = fetchRecentMsg(group_id, n)

#     if not last_messages:
#         await matcher.finish(messgae=Message("暂无记录"))

#     output = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(last_messages)])
#     ifIncluded, llmReply = await get_yulu_response(output)
#     try:
#         if ifIncluded == False:
#             not_found_path = os.path.normpath(os.path.join(assets_dir,"notFound.jpg"))
#             msg = Message(MessageSegment.image(not_found_path))
#         else:
#             llm_reply_path = os.path.normpath(os.path.join(assets_dir, "yulu", llmReply))
#             msg = Message(MessageSegment.image(llm_reply_path))
#         logger.debug(msg)
#         logger.debug(llmReply)
#         await matcher.finish(message=msg)
#     except nonebot.exception.FinishedException:
#         pass
#     except Exception as e:
#         logger.error(e)
#         await matcher.finish()

# revR = on_command("rev-r",priority=5, block=True)

# @revR.handle()
# async def revr(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
#     group_id = event.group_id
#     # if not event.user_id in Config.usr_whitelist:
#     #     await matcher.finish()

#     try:
#         n = int(str(args).strip()) if str(args).strip() else 5
#     except ValueError:
#         await matcher.finish(message=Message("格式错误，请输入 /rev-r[数字]"))

#     last_messages = fetchRecentMsg(group_id, n)

#     if not last_messages:
#         await matcher.finish(messgae=Message("暂无记录"))

#     output = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(last_messages)])
#     ifIncluded, llmReply = await get_yulu_response(output)
#     try:
#         if ifIncluded == False:
#             not_found_path = os.path.normpath(os.path.join(assets_dir,"notFound.jpg"))
#             msg = Message(MessageSegment.image(not_found_path))
#         else:
#             llm_reply_path = os.path.normpath(os.path.join(assets_dir, "yulu", llmReply))
#             llmReason = await get_yulu_reason(output, llmReply)
#             msg = Message([MessageSegment.image(llm_reply_path), MessageSegment.text(" " + llmReason)])
#             logger.debug(llmReason)
#         logger.debug(msg)
#         logger.debug(llmReply)
#         await matcher.finish(message=msg)
#     except nonebot.exception.FinishedException:
#         pass
#     except Exception as e:
#         logger.error(e)
#         await matcher.finish()

def usr_cd_check(user_id: str) -> bool:
    current_time = time.time()
    if user_id in Config.cooldown_whitelist:
        return True
    if user_id in cooldown_tracker:
        last_used = cooldown_tracker[user_id]
        if current_time - last_used < cooldown_period:
            return False
    cooldown_tracker[user_id] = current_time
    return True

he = on_regex(pattern=r"^我超.*盒$", priority=1)
@he.handle()
async def he_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    at = MessageSegment.at(event.get_user_id())
    if not usr_cd_check(event.get_user_id()):
        await he.finish()
    try:
        await he.finish(message=Message([at,MessageSegment.record(file=os.path.join(assets_dir, "he.mp3"))]))
    except nonebot.exception.FinishedException:
        pass
    except Exception as e:
        logger.error(e)

chishiL = on_regex(pattern=r"^吃史$", priority=1)
@chishiL.handle()
async def chishi(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    if not usr_cd_check(user_id):
        await chishiL.finish()
    if not Config.activate_eat:
        await chishiL.finish()
    await chishiL.finish(message=Message([at," 吃到了史"]))


EatL = on_regex(pattern=r"^吃饭$", priority=1)


@EatL.handle()
async def Eat(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    if not usr_cd_check(user_id):
        await EatL.finish()
    if not Config.activate_eat:
        await EatL.finish()
    Total_Assult_food = f"{random.choice(Config.Total_Assault_difficulty)}难度的{random.choice(Config.Total_Assault_bosslist)}"
    randFood = random.choice(Config.food+Config.stu)
    selected_food = random.choices([randFood, Total_Assult_food], weights=[85, 15], k=1)[0]
    msg = f" 吃到了{selected_food}。"
    await EatL.finish(message=Message([at, msg]))


Touxiang = on_regex(pattern=r"^投降$", priority=1)

@Touxiang.handle()
async def TouxiangL(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not usr_cd_check(user_id):
        await Touxiang.finish()
    msg = "🏳"
    await Touxiang.finish(message=Message([msg]))

Start_TotalAst = on_regex(pattern=r"^开票$", priority=1)


@Start_TotalAst.handle()
async def StartTotalAst(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    if not usr_cd_check(user_id):
        await Start_TotalAst.finish()
    if not Config.activate_TotalAst:
        await Start_TotalAst.finish()
    opt = ["炸票", "出分"]
    selected_difficulty = random.choices(Config.Total_Assault_difficulty, weights=[2, 2, 3, 3, 20, 50, 20], k=1)[0]
    Total_Assault = f" 打了{selected_difficulty}难度的{random.choice(Config.Total_Assault_bosslist)}，{random.choice(opt)}了。"
    await Start_TotalAst.finish(message=Message([at, Total_Assault]))


# pokeReact = on_notice()


# @pokeReact.handle()
# async def pokeReaction(bot: Bot, event: PokeNotifyEvent, state: T_State):
#     if not Config.activate_poke:
#         await pokeReact.finish()
#     if event.target_id == event.self_id:
#         at = MessageSegment.at(event.get_user_id())
#         msg = MessageSegment.text(" " + random.choice(Config.react))
#         await pokeReact.finish(message=Message([at, msg]))


RPluckyKing = on_notice()


@RPluckyKing.handle()
async def RPluckyKingFunc(bot: Bot, event: LuckyKingNotifyEvent, state: T_State):
    if not Config.activate_congrat:
        await RPluckyKing.finish()
    at = MessageSegment.at(event.get_user_id())
    msg = MessageSegment.text(" " + random.choice(Config.Congrats))
    await RPluckyKing.finish(message=Message([at, msg]))


# nao = on_regex(pattern=r"^闹了$", priority=1)


# @nao.handle()
# async def naoL(bot: Bot, event: GroupMessageEvent, state: T_State):
#     user_id = event.get_user_id()
#     at = MessageSegment.at(user_id)
#     if not usr_cd_check(user_id):
#         await nao.finish()
#     if llmCensor.recentMsgCensor(fetchRecentMsg(event.group_id,5),"不准闹") == False:
#         await nao.finish()
#     if event.group_id in Config.ai_group_whitelist:
#         if user_id == "853215637":
#             await nao.finish(message=Message([at," 就算是大王也不许闹！"]))
#         await nao.finish(message=Message([at, MessageSegment.image(os.path.join(assets_dir, "naole.png"))]))
#     else:
#         await nao.finish()


# aiyou = on_regex(pattern=r"^哎呦$", priority=1)


# @aiyou.handle()
# async def aiyouL(bot: Bot, event: GroupMessageEvent, state: T_State):
#     user_id = event.get_user_id()
#     at = MessageSegment.at(user_id)
#     if not usr_cd_check(user_id):
#         await aiyou.finish()
#     approveRep, llmReason = llmCensor.recentMsgCensor(fetchRecentMsg(event.group_id,5),"不准哎呦")
#     if approveRep == False:
#         Bot.send_private_msg(user_id=2447209382,message=llmReason)
#         await aiyou.finish()
#     if event.group_id in Config.ai_group_whitelist:
#         # logger.info(os.path.join(os.path.dirname(os.path.abspath(__file__)), "buxuaiyou.jpg"))
#         await aiyou.finish(message=Message([at, MessageSegment.image(os.path.join(assets_dir, "buxuaiyou.jpg"))]))
#     else:
#         await aiyou.finish()


# aiai = on_regex(pattern=r"^唉唉$", priority=1)


# @aiai.handle()
# async def aiaiL(bot: Bot, event: GroupMessageEvent, state: T_State):
#     user_id = event.get_user_id()
#     at = MessageSegment.at(user_id)
#     if not usr_cd_check(user_id):
#         await aiai.finish()
#     if event.group_id  not in Config.ai_group_whitelist:
#         await aiai.finish()
#     if user_id in Config.ai_usr_whitelist:
#         await aiai.finish()
#     approveRep, llmReason = llmCensor.recentMsgCensor(fetchRecentMsg(event.group_id,5),"不准唉唉")
#     if approveRep == False:
#         Bot.send_private_msg(user_id=2447209382,message=llmReason)
#         await aiai.finish()
#     else:
#         logger.info(os.path.join(assets_dir, "buzhunaiai.png"))
#         await aiai.finish(message=Message([at, MessageSegment.image(os.path.join(assets_dir, "buzhunaiai.png"))]))



# zhalan = on_regex(pattern=r"^栅栏$", priority=1)


# @zhalan.handle()
# async def zhalanL(bot: Bot, event: GroupMessageEvent, state: T_State):
#     user_id = event.get_user_id()
#     at = MessageSegment.at(user_id)
#     if not usr_cd_check(user_id):
#         await zhalan.finish()
#     if event.group_id in Config.ai_group_whitelist:
#         await zhalan.finish(message=Message([at, MessageSegment.image(os.path.join(assets_dir, "zhalan.jpg"))]))
#     else:
#         await zhalan.finish()


# haqi = on_regex(pattern=r"^哈气|哈氣|蛤气|哈気|哈汽|啥气|あくびをする|噺气$", priority=1)


# @haqi.handle()
# async def haqiL(bot: Bot, event: GroupMessageEvent, state: T_State):
#     user_id = event.get_user_id()
#     at = MessageSegment.at(user_id)
#     if not usr_cd_check(user_id):
#         await haqi.finish()
#     approveRep, llmReason = llmCensor.recentMsgCensor(fetchRecentMsg(event.group_id,5),"不准哈气")
#     if approveRep == False:
#         Bot.send_private_msg(user_id=2447209382,message=llmReason)
#         await haqi.finish()
#     if event.group_id in Config.ai_group_whitelist:
#         msg = " 哈气要交税！"
#         await haqi.finish(message=Message([at, msg]))
#     else:
#         await haqi.finish()

pinhaofan = on_regex(pattern=r"^拼好饭$", priority=1)


@pinhaofan.handle()
async def pin(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    if not usr_cd_check(user_id):
        await pinhaofan.finish()
    if not Config.activate_eat:
        await pinhaofan.finish()
    if random.random() < 0.05:
        msg = f" {at} 你的拼好饭被偷了！"
        await pinhaofan.finish(message=Message([msg]))
    if random.random() < 0.03:
        msg = f" {at} 很遗憾，人数太少拼团失败了"
        await pinhaofan.finish(message=Message([msg]))
    Total_Assult_food = f"{random.choice(Config.Total_Assault_difficulty)}难度的{random.choice(Config.Total_Assault_bosslist)}"
    randFood = random.choice(Config.food+Config.stu)
    selected_food = random.choices([randFood, Total_Assult_food], weights=[85, 15], k=1)[0]
    msg = f" 您与{random.randint(1,1052)}位群友一起拼到了{selected_food}，为您节省了{round(random.uniform(1,20),2)}元。"
    await pinhaofan.finish(message=Message([at, msg]))


baijian  = on_regex(pattern=r"速速拜见$", priority=1)
@baijian.handle()
async def baijianL(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    if user_id == "1051575616":
        await baijian.finish(message=Message([at," 拜见岁大王！"]))
    else:
        await baijian.finish()