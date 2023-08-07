from .StatuChecker import Check
from .DataManager import DataManage
from .BiliApi import Api
import asyncio
from nonebot.adapters.onebot.v11 import MessageSegment
from .MessageManager import MessageSender


class LivePush:

    def __init__(self) -> None:
        self.ck = Check()

    async def run(self):
        cookies = await self.ck.check_login()
        if cookies:
            with DataManage() as get:
                result = await get.acquire_live_push_uid()
            if result:
                uid_list: list = [i[0] for i in result]
                live_room_info_dict = await Api().get_room_info(uid_list)
                if live_room_info_dict:
                    await asyncio.gather(*[self.check_live_status(int(uid), room_info) for uid, room_info in live_room_info_dict.items()])

    async def check_live_status(self, uid: int, room_info: dict):
        """
        查看直播状态是否和数据库中一样,如果不一样,是否为1,为1则需要推送直播消息
        :param uid:
        :param room_info:
        :return:
        """
        new_live_status = room_info["live_status"]
        # logger.debug(f"查询 [{room_info['uname']}：{room_info['room_id']}] 开播信息中")
        with DataManage() as get:
            result = await get.acquire_live_status(uid)
        if new_live_status != result[0]:
            with DataManage() as modify:
                await modify.modify_live_status(uid, new_live_status)
            if new_live_status == 1:
                cover_link = room_info["cover_from_user"] or room_info["keyframe"]
                live_room_link = f"https://live.bilibili.com/{room_info['room_id']}"
                # logger.info(f"发现开播信息 ==> {room_info['uname']}")
                message = f"【{room_info['uname']}】开播啦!!!\n\n标题:{room_info['title']}\n\n传送门:{live_room_link}" \
                          f"\n{MessageSegment.image(cover_link)} "
                with DataManage() as get:
                    push_list = await get.acquire_live_push_info_by_uid(uid)
                tasks = [MessageSender().send_to(i[0], i[2], i[1], message)
                         for i in push_list]
                await asyncio.gather(*tasks)
