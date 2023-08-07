from nonebot import Bot
from typing import Union
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_command,on_notice
from nonebot.params import CommandArg
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message,GroupDecreaseNoticeEvent
from nonebot_plugin_guild_patch import GuildMessageEvent
from nonebot_plugin_guild_patch.permission import GUILD_ADMIN,GUILD_OWNER
from nonebot.adapters.onebot.v11 import GROUP_OWNER,GROUP_ADMIN
from nonebot import logger
from .Src.SignIn import Login
from .Src.SubManager import AddSub,DelSub,ModifySub,ShowSub
from .Src.BotSwitchManager import BotSwitchManage
from .Src.FollowListManager import FollowListManage
from .Src.DynamicManager import DynamicManage
from .Src.Other import OtherFunc

sign_in = on_command("登录", permission=SUPERUSER)


@sign_in.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await Login(bot, event).run()
    await sign_in.finish()

add_sub = on_command("添加",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))


@add_sub.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await AddSub(bot,event,str(args)).add_sub()
        await add_sub.finish()
    else:
        await add_sub.finish("请携带正确的UID")

del_sub = on_command("删除",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@del_sub.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await DelSub(bot,event,str(args)).del_sub()
        await del_sub.finish()
    else:
        await del_sub.finish("请携带正确的UID")

live_on = on_command("开启直播",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@live_on.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await ModifySub(bot,event,str(args),"live",1).run()
        await live_on.finish()
    else:
        await live_on.finish("请携带正确的UID")

live_off = on_command("关闭直播",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@live_off.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await ModifySub(bot,event,str(args),"live",0).run()
        await live_off.finish()
    else:
        await live_off.finish("请携带正确的UID")


dynamic_on = on_command("开启动态",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@dynamic_on.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await ModifySub(bot,event,str(args),"dynamic",1).run()
        await dynamic_on.finish()
    else:
        await dynamic_on.finish("请携带正确的UID")

dynamic_off = on_command("关闭动态",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@dynamic_off.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await ModifySub(bot,event,str(args),"dynamic",0).run()
        await dynamic_off.finish()
    else:
        await dynamic_off.finish("请携带正确的UID")

switch_on = on_command("开启机器人",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@switch_on.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]):
    await BotSwitchManage(bot,event).run(1)
    await switch_on.finish()

switch_off = on_command("关闭机器人",permission=(GROUP_ADMIN|GROUP_OWNER|SUPERUSER))

@switch_off.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]):
    await BotSwitchManage(bot,event).run(0)
    await switch_off.finish()

cancel_follow = on_command("取消关注", permission=SUPERUSER)

@cancel_follow.handle()
async def _(bot:Bot,event:GroupMessageEvent, args: Message = CommandArg()):
    if args and str(args).isdigit():
        await FollowListManage(bot,event).del_follow(str(args))
        await cancel_follow.finish()
    else:
        await cancel_follow.finish("请携带正确的UID")

refresh_follow = on_command("刷新关注",permission=SUPERUSER)
async def _(bot:Bot,event:GroupMessageEvent):
    result = await FollowListManage(bot,event).refresh_follow_list()
    if isinstance(result,str):
        await refresh_follow.finish(result)
    else:
        await refresh_follow.finish()

driver=get_driver()

@driver.on_startup
async def refresh_all_follow():
    logger.info("正在刷新关注列表")
    await FollowListManage().refresh_follow_list()

@driver.on_startup
async def _():
    logger.info("正在更新动态数据")
    await DynamicManage().refresh_dynamic_id()


decrease_group = on_notice()

@decrease_group.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    if bot.self_id == str(event.user_id):
        await DelSub(bot,event).del_sub_by_position()
    await decrease_group.finish()


show_sub = on_command("列表")

@show_sub.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]):
    await ShowSub(bot,event).get_all_sub()
    await show_sub.finish()

help_p = on_command("帮助")

@help_p.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]):
    await OtherFunc(bot,event).help()
    await help_p.finish()

find_dynamic = on_command("查看动态")

@find_dynamic.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args and str(args).isdigit():
        await OtherFunc(bot,event).find_dynamic(str(args))
        await find_dynamic.finish()
    else:
        await find_dynamic.finish("请携带正确的参数")

analyze_link = on_command("解析")

@analyze_link.handle()
async def _(bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent], args: Message = CommandArg()):
    if args:
        await OtherFunc(bot,event).analyze_short_link(str(args))
        await analyze_link.finish()
    else:
        await analyze_link.finish("请携带正确的短链接")