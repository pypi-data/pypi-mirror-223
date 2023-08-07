from typing import Union,Optional
from nonebot import Bot
import json
from .DataManager import DataManage
from .DataManager.FollowManager import FollowManage
from .DataManager.CookieManager import CookieManage
from .StatuChecker import Check
from nonebot.adapters.onebot.v11 import GroupMessageEvent,MessageSegment
from nonebot_plugin_guild_patch import GuildMessageEvent
from .BiliApi import Api
from .BotSwitchManager import SwitchManage
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from os import path


class AddSub:
    def __init__(self,bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent],uid:str) -> None:
        self.bot = bot
        self.event = event
        self.uid = uid
        self.checker = Check(bot,event)
    

    async def add_sub(self):
        # 查询是否开启了bot开关
        r =await  self.checker.get_statu()
        if r:
            # 查询是否有cookie
            if await self.checker.check_login():
                if self.event.message_type == "group":
                    position = str(self.event.group_id)
                else:
                    position = json.dumps(
                        {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
                    )
                bot_id = self.bot.self_id
                # 查询是否订阅过
                with DataManage() as get_sub:
                    result = await get_sub.acquire_sub_info_by_uid(self.uid,position,bot_id)
                if result:
                    await self.bot.send(self.event,"请勿重复订阅")
                # 没订阅过
                else:
                    # 查询是否关注了
                    with FollowManage() as get_follow:
                       result = await get_follow.get_follow_by_uid(self.uid)
                    # 关注了
                    if result:
                        with DataManage() as store:
                            await store.store_sub_info(result[0],result[1],0,position,bot_id,self.event.message_type)
                        await self.bot.send(self.event,f"成功订阅 --> {result[1]}({result[0]})")
                    # 没关注
                    else:
                        api = Api()
                        # 获取cookie
                        with CookieManage() as get_cookie:
                            result = await get_cookie.acquire_cookie()
                        cookie_dict = json.loads(result[0])
                        # 获取uid的信息
                        uid_info = await api.get_uid_info(self.uid)
                        # 获取到了uid的信息的话
                        if uid_info:
                            # 关注
                            follow_result = await api.change_follow(self.uid,1,cookie_dict)
                            if isinstance(follow_result,str):
                                await self.bot.send(self.event,follow_result)
                            else:
                                uname = uid_info["nick_name"]
                                # 先将uid对应的信息存在关注列表
                                with FollowManage() as store:
                                    await store.store_follow_info(self.uid,uname)
                                # 存储订阅信息
                                with DataManage() as store_sub:
                                    await store_sub.store_sub_info(self.uid,uname,uid_info["liveStatus"],position,bot_id,self.event.message_type)
                                await self.bot.send(self.event,f"成功订阅 --> {uname}({self.uid})")
                        else:
                            await self.bot.send(self.event,f"未获取到uid: {self.uid} 的信息")
            else:
                await self.bot.send(self.event,"未登录，请联系管理员")


class DelSub:
    def __init__(self,bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent],uid:Optional[str]=None) -> None:
        self.bot = bot
        self.event = event
        self.uid = uid
        self.checker = Check(bot,event)
    

    async def del_sub(self):
        # 查询是否开启了bot开关
        r = await self.checker.get_statu()
        if r:
            # 查询是否有cookie
            if await self.checker.check_login():
                if self.event.message_type == "group":
                    position = str(self.event.group_id)
                else:
                    position = json.dumps(
                        {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
                    )
                bot_id = int(self.bot.self_id)
                # 查询是否订阅过
                with DataManage() as get_sub:
                    result = await get_sub.acquire_sub_info_by_uid(self.uid,position,bot_id)
                # 订阅过先删除订阅
                if result:
                    with DataManage() as delete_sub:
                        await delete_sub.del_sub_info_by_uid(self.uid,self.bot.self_id,position)
                    await self.bot.send(self.event,f"成功删除 --> {self.uid}")
                else:
                    await self.bot.send(self.event,f"未订阅过 --> {self.uid}")
            else:
                await self.bot.send(self.event,"未登录，请联系管理员")
    
    async def del_sub_by_position(self):
        position = str(self.event.group_id)
        bot_id = self.bot.self_id
        with DataManage() as del_data:
            await del_data.del_sub_info_by_position(bot_id,position)
        with SwitchManage() as del_switch:
            await del_switch.del_SwitchStatus(position,bot_id)
        
        

class ModifySub:
    def __init__(self,bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent],uid:str,modify_type:str,action:int) -> None:
        self.bot = bot
        self.event = event
        self.uid = uid
        self.modify_type = modify_type
        self.action = action
        self.checker = Check(bot,event)
    
    async def run(self):
        r =await self.checker.get_statu()
        if r:
            if self.event.message_type == "group":
                position = str(self.event.group_id)
            else:
                position = json.dumps(
                    {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
                )
            if self.modify_type == "live":
                await self.modify_live(position)
            else:
                await self.modify_dynamic(position)


    async def modify_live(self,position):
        with DataManage() as get:
            result = await get.acquire_sub_info_by_uid(self.uid,position,self.bot.self_id)
        if result:
            if result[3] == self.action:
                text = "关闭" if self.action == 0 else "开启"
                await self.bot.send(self.event,f"请勿重复{text}直播推送")
            else:
                origin_statu = "关闭" if result[3] ==0 else "开启"
                new_statu = "关闭" if self.action ==0 else "开启"
                with DataManage() as modify:
                    await modify.modify_live_on(self.uid,self.bot.self_id,position,self.action)
                await self.bot.send(self.event,f"直播推送({self.uid})\n\n{origin_statu} --> {new_statu}")
        else:
            await self.bot.send(self.event,f"未订阅 --> {self.uid}")
        


    async def modify_dynamic(self,position):
        with DataManage() as get:
            result = await get.acquire_sub_info_by_uid(self.uid,position,self.bot.self_id)
        if result:
            if result[4] == self.action:
                text = "关闭" if self.action == 0 else "开启"
                await self.bot.send(self.event,f"请勿重复{text}动态推送")
            else:
                origin_statu = "关闭" if result[4] ==0 else "开启"
                new_statu = "关闭" if self.action ==0 else "开启"
                with DataManage() as modify:
                    await modify.modify_dynamic_on(self.uid,self.bot.self_id,position,self.action)
                await self.bot.send(self.event,f"动态推送({self.uid})\n\n{origin_statu} --> {new_statu}")
        else:
            await self.bot.send(self.event,f"未订阅 --> {self.uid}")


class ShowSub:
    def __init__(self,bot:Bot,event:Union[GroupMessageEvent,GuildMessageEvent]) -> None:
        self.bot = bot
        self.event = event
        self.checker = Check(bot,event)

    async def get_all_sub(self):
        r = await self.checker.get_statu()
        if r:
            if self.event.message_type == "group":
                        position = str(self.event.group_id)
            else:
                position = json.dumps(
                    {"guild_id": self.event.guild_id, "channel_id": self.event.channel_id}
                )
            bot_id = self.bot.self_id
            with DataManage() as get:
                all_sub = await get.acquire_sub_info_by_position(bot_id,position)
            if not all_sub:
                await self.bot.send(self.event, "订阅列表为空")
            else:
                img = MessageSegment.image(await self.make_pic(all_sub))
                await self.bot.send(self.event, img)
        

    async def make_pic(self,sub_list: list):
        """制作订阅列表图片

        Args:
            sub_list (list): 订阅列表

        Returns:
            bytes: 图片的二进制
        """
        title_info = ["UID", "昵称", "动态推送", "直播推送"]
        font = ImageFont.truetype(
            path.join(path.dirname(path.abspath(__file__)), "Static", "HanaMinA.ttf"), 25
        )
        title_image = Image.new("RGB", (1200, 50), (255, 255, 255, 255))
        draw = ImageDraw.Draw(title_image)
        # 制作表头框
        for i in range(4):
            draw.rectangle(
                (300 * i, 0, 300 * (i + 1), 50), fill=None, outline=(0, 0, 0), width=2
            )
        # 制作表头
        for j in range(4):
            x = ((300 - font.getsize(str(title_info[j]))[0]) / 2) + 300 * j
            y = (50 - font.getsize(str(title_info[j]))[1]) / 2
            draw.text((x, y), text=str(title_info[j]), fill="black", font=font)
        img_list = [title_image]
        for sub_detail in sub_list:
            img_new = Image.new("RGB", (1200, 50), (255, 255, 255, 255))
            draw = ImageDraw.Draw(img_new)
            for x in range(4):
                draw.rectangle(
                    (300 * x, 0, 300 * (x + 1), 50), fill=None, outline=(0, 0, 0), width=2
                )
            uid = str(sub_detail[0])
            draw.text(
                (((300 - font.getsize(uid)[0]) / 2), (50 - font.getsize(uid)[1]) / 2),
                uid,
                fill="black",
                font=font,
            )
            name = str(sub_detail[1])
            draw.text(
                (
                    ((300 - font.getsize(name)[0]) / 2) + 300,
                    (50 - font.getsize(name)[1]) / 2,
                ),
                name,
                fill="black",
                font=font,
            )
            dynamic_on = "关" if sub_detail[4] == 0 else "开"
            color = "red" if dynamic_on == "关" else "black"
            draw.text(
                (
                    ((300 - font.getsize(dynamic_on)[0]) / 2) + 600,
                    (50 - font.getsize(dynamic_on)[1]) / 2,
                ),
                dynamic_on,
                fill=color,
                font=font,
            )
            live_on = "关" if sub_detail[3] == 0 else "开"
            color = "red" if live_on == "关" else "black"
            draw.text(
                (
                    ((300 - font.getsize(live_on)[0]) / 2) + 900,
                    (50 - font.getsize(live_on)[1]) / 2,
                ),
                live_on,
                fill=color,
                font=font,
            )
            img_list.append(img_new)
        img_h = len(img_list) * 50
        combination = Image.new("RGB", (1200, img_h), (255, 255, 255))
        for i in range(len(img_list)):
            combination.paste(img_list[i], (0, 50 * i))
        img_byte = BytesIO()
        combination.save(img_byte, format="PNG")
        return img_byte.getvalue()