from .StatuChecker import Check
from .DataManager import DataManage
from .BiliApi import Api
import asyncio
import json
from nonebot import logger
from bilirpc.api import get_follow_dynamic,get_dy_detail
from nonebot.adapters.onebot.v11 import MessageSegment
from .MessageManager import MessageSender
from google.protobuf.json_format import MessageToJson
import skia
from dynrender_skia.Core import DynRender
from io import BytesIO
from dynamicadaptor.DynamicConversion import formate_message


class DynPush:
    def __init__(self) -> None:
        self.ck = Check()
    
    async def run(self):
        cookies =await self.ck.check_login()
        if cookies:
            try:
                cookie = cookies["cookie"]
                await self.web_push(cookie)
            except Exception as e:
                token = cookies["access_token"]
                await self.grpc_push(token)


    async def grpc_push(self,token):
        all_dynamic = await get_follow_dynamic(token)
        if all_dynamic:
            tasks = [self.check_push(dynamic) for dynamic in all_dynamic]
            await asyncio.gather(*tasks)
            

    async def check_push(self, dynamic):
        """检查是否有群订阅
        :param dynamic: 动态主体
        :type dynamic: DynamicItem
        """
        dynamic_id = dynamic.extend.dyn_id_str
        # logger.info(dynamic.card_type)
        # logger.debug(f"检测到动态:{dynamic.extend.orig_name} --> ({dynamic_id})")
        with DataManage() as get:
            all_dy_id = await get.acquire_dynamic_id(dynamic_id)
        if not all_dy_id:
            uid = dynamic.extend.uid
            dynamic_str = MessageToJson(dynamic)
            uname = dynamic.modules[0].module_author.author.name
            with DataManage() as store:
                await store.store_dynamic_id(dynamic_id,uname,dynamic_str,uid,"grpc")
            with DataManage() as get:
                # await get.store_dynamic_id(dynamic_id)
                push_info = await get.acquire_dynamic_push_info_by_uid(uid)
            if push_info:
                # 动态可能为被折叠类型
                if dynamic.card_type == 5:
                    logger.info(f"检测到被折叠动态:{dynamic_id}")
                    result = await get_dy_detail(dynamic_id)
                    dynamic = result[0]
                module_type_list = [i.module_type for i in dynamic.modules]
                # 动态下含有其他被折叠的动态
                if 10 in module_type_list and (dynamic.modules[module_type_list.index(10)].module_fold.fold_type == 3):
                    fold_ids: str = dynamic.modules[module_type_list.index(10)].module_fold.fold_ids
                    fold_dynamics = await get_dy_detail(fold_ids)
                    await asyncio.gather(*[self.check_push(i) for i in fold_dynamics])
                logger.info(
                    f"检测到新动态:{dynamic.modules[0].module_author.author.name} --> ({dynamic_id})"
                )
                message = await formate_message("grpc",json.loads(dynamic_str))
                img = await DynRender().run(message)
                img = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
                logger.info("grpc渲染图片完成")
                img_byte = BytesIO()
                img.save(img_byte)
                img = img_byte.getvalue()
                logger.info("grpc 图片获取bytes成功")
                # self.bot.send(self.event,MessageSegment.image(img_byte.getvalue()))
                url = f"https://t.bilibili.com/{dynamic.extend.dyn_id_str}"
                name = push_info[0][0]
                type_msg = {
                    6: "发布了新动态",
                    7: "发布了图片动态",
                    2: "发布了新投稿视频",
                    18: "发布了直播动态",
                    12: "发布了直播动态",
                    8: "发布了新专栏",
                    11: "发布了新动态",
                    14: "发布了付费课程",
                    13: "分享了收藏夹",
                    3: "发布了新专辑",
                    9: "发布了新音乐",
                    10: "发布了新动态",
                    1: "转发了一条动态",
                }
                message = (
                    f"{name}"
                    + f"{type_msg.get(dynamic.card_type, type_msg[6])}:\n\n"
                    + "传送门→"
                    + f"{url}"
                    + "\n"
                    + MessageSegment.image(img)
                )
                
                tasks = [
                    MessageSender().send_to(i[1], i[3], i[2], message) for i in push_info
                ]
                logger.info("grpc 发送图片")
                await asyncio.gather(*tasks)

    async def web_push(self,cookie):
        all_dynamic = await Api().get_follow_dynamic(cookie)
        if all_dynamic:
            tasks = [self.check_push_web(dynamic) for dynamic in all_dynamic]
            await asyncio.gather(*tasks)
    
    async def check_push_web(self,dynamic):
        dynamic_id = dynamic["id_str"]
        name = dynamic["modules"]["module_author"]["name"]
        uid = dynamic["modules"]["module_author"]["mid"]
        # logger.debug(f"检测到动态:{name} --> ({dynamic_id})")
        with DataManage() as get:
            all_dy_id = await get.acquire_dynamic_id(dynamic_id)
        if not all_dy_id:
            with DataManage() as get:
                await get.store_dynamic_id(dynamic_id,name,json.dumps(dynamic),uid,"web")
                push_info = await get.acquire_dynamic_push_info_by_uid(uid)
            if push_info and dynamic["type"] != "DYNAMIC_TYPE_LIVE_RCMD":
                logger.info(f"检测到新动态:{name} --> ({dynamic_id})")
                message =await formate_message("web",dynamic)
                if message is not None:
                    img = await DynRender().run(message)
                    img = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
                    logger.info("渲染图片完成")
                    img_byte = BytesIO()
                    img.save(img_byte)
                    img = img_byte.getvalue()
                    image = MessageSegment.image(img)
                else:
                    image = "[图片]"
                url = f"https://t.bilibili.com/{dynamic_id}"
                name = name

                message = (
                    f"{name}"
                    + "发布了新动态:\n\n"
                    + "传送门→"
                    + f"{url}"
                    + "\n"
                    + image
                )
                tasks = [
                    MessageSender().send_to(i[1], i[3], i[2], message) for i in push_info
                ]
                logger.info("发送成功")
                await asyncio.gather(*tasks)
