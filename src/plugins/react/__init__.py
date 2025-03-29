import random, os, time
from nonebot import on_notice, on_regex
from nonebot.typing import T_State
from nonebot import logger
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, LuckyKingNotifyEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.rule import fullmatch
from .config import Config

EatL = on_regex(pattern=r"^吃饭$", priority=1)

cooldown_tracker = {}
cooldown_period = Config.cooldown_period

@EatL.handle()
async def Eat(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    current_time = time.time()
    at = MessageSegment.at(event.get_user_id())

    if user_id in cooldown_tracker:
        last_used = cooldown_tracker[user_id]
        if current_time - last_used < cooldown_period:
            remaining_time = cooldown_period - (current_time - last_used)
            await EatL.finish()
    cooldown_tracker[user_id] = current_time

    if not Config.activate_eat:
        await EatL.finish()
    randList = Config.food + Config.stu
    msg = f" 吃到了{random.choice(randList)}。"
    await EatL.finish(message=Message([at,msg]))


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
    user_id = event.get_user_id()
    current_time = time.time()
    at = MessageSegment.at(event.get_user_id())

    if user_id in cooldown_tracker:
        last_used = cooldown_tracker[user_id]
        if current_time - last_used < cooldown_period:
            remaining_time = cooldown_period - (current_time - last_used)
            await nao.finish()
    cooldown_tracker[user_id] = current_time

    if event.group_id == 996101999 or event.group_id == 225173408:
        await nao.finish(message = Message([at,MessageSegment.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "naole.png"))]))
    else:
        await nao.finish()


aiyou = on_regex(pattern=r"^哎呦$", priority=1)

@aiyou.handle()
async def aiyouL(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    current_time = time.time()
    at = MessageSegment.at(event.get_user_id())

    if user_id in cooldown_tracker:
        last_used = cooldown_tracker[user_id]
        if current_time - last_used < cooldown_period:
            remaining_time = cooldown_period - (current_time - last_used)
            await aiyou.finish()
    cooldown_tracker[user_id] = current_time

    if event.group_id == 996101999 or event.group_id == 225173408:
        logger.info(os.path.join(os.path.dirname(os.path.abspath(__file__)), "buxuaiyou.jpg"))
        await aiyou.finish(message = Message([at,MessageSegment.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "buxuaiyou.jpg"))]))
    else:
        await aiyou.finish()


aiai = on_regex(pattern=r"^唉唉$", priority=1)

@aiai.handle()
async def aiaiL(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    current_time = time.time()
    at = MessageSegment.at(event.get_user_id())

    if user_id in cooldown_tracker:
        last_used = cooldown_tracker[user_id]
        if current_time - last_used < cooldown_period:
            remaining_time = cooldown_period - (current_time - last_used)
            await aiai.finish()
    cooldown_tracker[user_id] = current_time

    if event.group_id in Config.aiai_group and event.get_user_id() not in str(Config.aiai_usr):
        logger.info(os.path.join(os.path.dirname(os.path.abspath(__file__)), "buzhunaiai.jpg"))
        await aiai.finish(message = Message([at,MessageSegment.image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "buzhunaiai.jpg"))]))
    else:
        await aiai.finish()