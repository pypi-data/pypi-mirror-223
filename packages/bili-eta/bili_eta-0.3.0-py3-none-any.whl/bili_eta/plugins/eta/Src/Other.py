from os import path
from typing import Union
from nonebot import Bot
from io import BytesIO
import json
import re
from .BiliApi import Api
from .DataManager import DataManage
from google.protobuf.json_format import MessageToJson
from dynamicadaptor.DynamicConversion import formate_message
from bilirpc.api import get_dy_detail, get_space_dynamic
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot_plugin_guild_patch import GuildMessageEvent
from dynrender_skia.Core import DynRender
from .StatuChecker import Check
import skia

class OtherFunc:
    def __init__(self, bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]) -> None:
        self.bot = bot
        self.event = event
        self.ck = Check(self.bot,self.event)

    async def help(self):
        pic_path = path.join(path.dirname(
            path.abspath(__file__)), "Static", "help.png")
        with open(pic_path, "rb") as f:
            pic = f.read()
        message = MessageSegment.image(pic)
        await self.bot.send(self.event, message)

    async def find_dynamic(self, arg):
        status = await self.ck.get_statu()
        if status:
            if len(arg) > 16:
                with DataManage() as get:
                    result = await get.acquire_dynamic_by_dyn_id(arg)
                # 如果本地存的有
                if result:
                    dyn_type = result[1]
                    message = await formate_message(dyn_type, json.loads(result[3]))
                    img =await DynRender().run(message)
                    img = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
                    img_byte = BytesIO()
                    img.save(img_byte)
                    await self.bot.send(self.event,MessageSegment.image(img_byte.getvalue()))
                # 本地存的没有
                else:
                    # 查询B站动态
                    dynamic_detail = await Api().get_dynamic_detail(arg)
                    # 如果查到了
                    if dynamic_detail:
                        dynamic = dynamic_detail["data"]["item"]
                        dynamic_str = json.dumps(dynamic)
                        message = await formate_message("web",dynamic)
                        with DataManage() as store:
                            await store.store_dynamic_id(message.message_id,message.header.name, dynamic_str, message.header.mid, "web")
                        img =await DynRender().run(message)
                        img = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)                        
                        img_byte = BytesIO()
                        img.save(img_byte)
                        await self.bot.send(self.event,MessageSegment.image(img_byte.getvalue()))
                    else:
                        await self.bot.send(self.event, "未找到动态")

    async def analyze_short_link(self,link):
        status = await self.ck.get_statu()
        if status:
            result = re.match(r"(.*?)://b23.tv/(\S+)",link)
            if result:
                location = await Api().get_location(link)
                if location:
                    result = re.match(r"https://m.bilibili.com/dynamic/(\d+)",location)
                    result_2 = re.match(r"https://t.bilibili.com/(\d+)",location)
                    if result:
                        dynamic_id = result.group(1)
                        await self.find_dynamic(dynamic_id)
                    elif result_2:
                        dynamic_id = result_2.group(1)
                        await self.find_dynamic(dynamic_id)
                    else:
                        await self.bot.send(self.event,"解析失败,未查询到相应的动态id")
                else:
                    await self.bot.send(self.event,"解析失败，请输入正确的短链接")
