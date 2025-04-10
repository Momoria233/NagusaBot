from typing import Dict


class Config:
    # 目前允许的格式：
    # 1. {at} 对加群人的 at
    # 2. {img:path} 路径为 path 的图片

    welcome_message: Dict[int, str] = {
        996101999: "欢迎{at} 老师来到北京BAO游客群！\n请老师先阅读群公告，有问题请私信群管理\n目前北京bao2.0仍未开票，当前bilibili上开票的京b2.0并非本展！\n请老师敬请期待，也祝老师在群里玩得愉快！",
        225173408: "入群测试消息",
    }
