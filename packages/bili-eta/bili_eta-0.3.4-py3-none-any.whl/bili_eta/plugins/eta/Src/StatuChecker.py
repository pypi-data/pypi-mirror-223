from .DataManager.CookieManager import CookieManage
from .DataManager.SwitchManager import SwitchManage
from nonebot import Bot
from  typing import Union,Optional
import json
import time
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

class Check:
    def __init__(self,bot:Optional[Bot]=None,event:Union[GuildMessageEvent,GroupMessageEvent,None]=None) -> None:
        self.bot:Optional[Bot] = bot
        self.event:Union[GuildMessageEvent,GuildMessageEvent,None] = event

    async def get_statu(self):
        if self.event.message_type == "group":
            position = str(self.event.group_id)
        else:
            position = json.dumps(
                {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
            )
        bot_id = int(self.bot.self_id)
        with SwitchManage() as switch_getter:
            switch = await switch_getter.acquire_SwitchStatus(position, bot_id)
        if switch:
            return switch[0] == 1
        with SwitchManage() as switch_setter:
            await switch_setter.store_SwitchStatus(position, bot_id)
        return True

    async def check_login(self):
        with CookieManage() as get:
            cookie_info = await get.acquire_cookie()
        if not cookie_info:
            return False
        if cookie_info[3] > int(time.time()):
            return {"cookie": json.loads(cookie_info[0]), "access_token": cookie_info[1],"mid":cookie_info[4]}
        else:
            with CookieManage() as d_cookie:
                await d_cookie.delete_old_cookie()
            return False

    
