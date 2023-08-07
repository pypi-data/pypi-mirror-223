from typing import Union
from nonebot import Bot
import json
from .DataManager.SwitchManager import SwitchManage
from .StatuChecker import Check
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent


class BotSwitchManage:
    def __init__(self,bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]) -> None:
        self.bot = bot
        self.event = event
        self.checker = Check(bot,event)
    
    async def run(self,action):
        if self.event.message_type == "group":
            position = str(self.event.group_id)
        else:
            position = json.dumps(
                {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
            )
        if await self.checker.get_statu():
            if action == 1:
                await self.bot.send(self.event,"当前机器人已为开启状态")
            else:
                with SwitchManage() as s_off:
                    await s_off.modify_SwitchStatus(position,self.bot.self_id,0)
                await self.bot.send(self.event,"机器人已关闭")
        else:
            if action == 1:
                with SwitchManage() as s_off:
                    await s_off.modify_SwitchStatus(position,self.bot.self_id,1)
                await self.bot.send(self.event,"机器人已开启")

