import random, os, json
from nonebot import on_notice, on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, LuckyKingNotifyEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from .config import Config

EatL = on_regex(pattern=r"^吃饭$", priority=1)


@EatL.handle()
async def Eat(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not Config.activate_eat:
        await EatL.finish()
    randList = Config.food + Config.stu
    msg = f"吃到了{random.choice(randList)}。"
    await EatL.finish(message=Message(msg))


pokeReact = on_notice()


@pokeReact.handle()
async def pokeReaction(bot: Bot, event: PokeNotifyEvent, state: T_State):
    if not Config.activate_poke:
        await pokeReact.finish()
    if event.target_id == event.self_id:
        at = MessageSegment.at(event.get_user_id())
        msg = MessageSegment.text(" " + random.choice(Config.react))
        await pokeReact.finish(message=Message([at, msg]))


RPluckyKing = on_notice()


@RPluckyKing.handle()
async def RPluckyKingFunc(bot: Bot, event: LuckyKingNotifyEvent, state: T_State):
    if not Config.activate_congrat:
        await RPluckyKing.finish()
    at = MessageSegment.at(event.get_user_id())
    msg = MessageSegment.text(" " + random.choice(Config.Congrats))
    await pokeReact.finish(message=Message([at, msg]))


nao = on_regex(pattern=r"^闹了$", priority=1)


@nao.handle()
async def naoL(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not Config.activate_nao:
        nao.finish()
    if event.group_id == 996101999 or event.group_id == 225173408:
        await nao.finish(MessageSegment.image(os.path.join(os.path.abspath(__file__), "naole.png")))
    else:
        await nao.finish()
