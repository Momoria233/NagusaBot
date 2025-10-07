from typing import Dict

class Config:
    # 目前允许的格式：
    # 1. {at} 对加群人的 at
    # 2. {img:path} 路径为 path 的图片
    # 3. {file:path} 路径为 path 的文件
    # 4. {countdown:YYYY-MM-DD} 距离 YYYY-MM-DD 的倒计时

    welcome_message: Dict[int, str] = {
        # 996101999: "欢迎{at} 老师来到北京BAO游客群！\n请老师先阅读群公告，有问题请私信群管理\n本展已于会员购开票，链接为show.bilibili.com/platform/detail.html?id=101173。\n注意：本展与目前会员购上另一个“北京BAO2.0”并非同一个展，请老师购票时注意分辨。\n最后，请老师敬请期待，也祝老师在群里玩得愉快！{img:welcomeT.jpg}",
        996101999: "欢迎{at} 老师来到北京BAO游客群！\n请老师先阅读群公告，有问题请私信群管理\n北京bao2.0已经圆满结束，感谢各位老师支持，也期待与各位老师的下次相见！{img:2.0endWelcome.png}",
        225173408: "哼哼，{at}老师，欢迎来到天津蔚Only游客群哦！\n先请老师仔细阅读群公告，如有任何问题请及时联系群管理，我们便利屋68会为老师解决任何问题。\n距离任务开始还有{countdown:2026-01-24}，还请老师期待着我们的活动，也祝老师在这里玩的愉快呢！{img:tianjinWelcome.jpg}",
        # 929799205: ""
    }
