import nonebot
import json
from typing import Optional
from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, Bot, Message
from nonebot_plugin_guild_patch import GuildMessageEvent


class MessageSender:
    def __init__(self):
        self.__bot = None
        self.__message = None
        self.__send_method = {
            "group": self.__send_group_message,
            "guild": self.__send_guild_message,
        }

    async def send_to(
        self, bot_id: str, send_type: str, position: str, message
    ) -> None:
        # sourcery skip: raise-specific-error
        try:
            self.__bot = nonebot.get_bot(self_id=bot_id)
            self.__message = message
            if send_type == "group":
                logger.info(f"Bot:{bot_id} ==> 将发送消息至群:{position}")
                await self.__send_method[send_type](int(position))
            elif send_type == "guild":
                position_js = json.loads(position)
                guild_id = position_js["guild_id"]
                channel_id = position_js["channel_id"]
                logger.info(f"Bot:{bot_id}==> 将发送消息至频道:{guild_id}==>子频道:{channel_id}")
                await self.__send_method[send_type](guild_id, channel_id)
            else:
                raise Exception("Unknown message type")
        except KeyError:
            logger.error(f"Bot未连接 ==> {bot_id}")

    async def __send_guild_message(
        self, guild_id: Optional[int] = None, channel_id: Optional[int] = None
    ) -> None:
        try:
            await self.__bot.call_api(
                "send_guild_channel_msg",
                **{
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "message": self.__message,
                },
            )
        except Exception as e:
            logger.exception("What?!")

    async def __send_group_message(self, group_id: Optional[int] = None) -> None:
        try:
            await self.__bot.call_api(
                "send_group_msg", **{"group_id": group_id, "message": self.__message}
            )
        except Exception as e:
            logger.exception("What?!")