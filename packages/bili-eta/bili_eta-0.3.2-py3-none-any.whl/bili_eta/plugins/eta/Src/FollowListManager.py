from typing import Union
from nonebot import Bot
import json
from .DataManager import DataManage
from .DataManager.FollowManager import FollowManage
from .DataManager.CookieManager import CookieManage
from .StatuChecker import Check
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent
from .BiliApi import Api


class FollowListManage:
    def __init__(self,bot:Union[Bot,None]=None,event:Union[GroupMessageEvent,GuildMessageEvent,None]=None) -> None:
        self.bot = bot
        self.event = event
        self.checker = Check(bot,event)
    
    async def del_follow(self,uid:str):
        cookies =await self.checker.check_login()
        if cookies:
            cookie = cookies["cookie"]
            with FollowManage() as get:
                result = await get.get_follow_by_uid(uid)
            if result:
                api = Api()
                change_follow_result = await api.change_follow(uid,2,cookie)
                if isinstance(change_follow_result,str):
                    await self.bot.send(self.event,change_follow_result)
                else:
                    with FollowManage() as del_follow:
                        await del_follow.delete_follow(uid)
                    with DataManage() as del_sub:
                        await del_sub.del_all_sub_by_uid(uid)
                    
                    await self.bot.send(self.event,f"成功取关 --> {uid}")
            else:
                await self.bot.send(self.event,f"未关注 --> {uid}")
        else:
            await self.bot.send(self.event,"未登录")
    

    async def refresh_follow_list(self):
        cookies = await self.checker.check_login()
        if cookies:
            cookie = cookies["cookie"]
            uid = cookies["mid"]
            api = Api()
            follow_info = []
            for i in range(40):
                page = i+1
                all_follow_info = await api.get_follow_list(uid,cookie,page)
                if all_follow_info:
                    follow_info.extend(all_follow_info)
                    page+=1
                else:
                    break
            all_follow_info = follow_info
            if isinstance(all_follow_info,list) and all_follow_info:
                with FollowManage() as d:
                    await d.del_all_follow()
                with FollowManage() as w:
                    for i in all_follow_info:
                        await w.store_follow_info(i["mid"],i["uname"])
                with DataManage() as w:
                    for i in all_follow_info:
                        await w.modify_name(i["mid"],i["uname"])
                return True
            else:
                return "获取关注列表失败"
        else:
            return "未登录"


    

    