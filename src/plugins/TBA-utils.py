from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupDecreaseNoticeEvent,
    GroupRequestEvent,
    Message,
)
from nonebot.typing import T_State

# from nonebot.adapters.onebot.v12 import GroupNameChangeEvent #这行代码仅供展示 跑不通


"""
以下为来自第一个可运行版本的留言 有点古老了




这里是一些在https://onebot.adapters.nonebot.dev/docs/api/v11/index以及https://github.com/botuniverse/onebot-11/blob/master/event/README.md找到的有趣的事件
如果之后有相应想法的话可以扩充成单独的plugin

GroupRequestEvent是在有人申请加群的时候触发的事件 可以单独汇报给管理员
但是考虑到qq已经有相关功能了所以可以不用写

GroupDecreaseNoticeEvent是在有人退群的时候触发的事件 但是好像写了也没什么用就先放在这里了

其实AL-1s有一个生日@生日快乐然后回复感谢的功能 但是我们至今不知道名草的生日是哪一天 残念。
不过其实做个学生生日播报也是可以的...?
唔 有时间再说

还有一个GroupNameChangeEvent 这不是onebot v11的标准import名称 但是在Lagrange里面是这么汇报的
想的是可以等倒计时时候写 但是转念一想其实到时候人工上号播报也可以（

剩下可能还有不少有趣的功能 有些没加的是我还没来得及细看 有些是我感觉加了确实没啥意义 之后有时间再说吧

哦对 至于票务通知
这个没太get到具体要写的是什么 不过通知类的其实最方便的就是直接人工上号at所有人

"""
