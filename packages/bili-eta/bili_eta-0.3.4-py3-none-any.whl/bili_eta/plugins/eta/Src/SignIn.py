import qrcode
import time
import json
import asyncio
from io import BytesIO
from nonebot import Bot
from nonebot import logger
from .BiliApi import TvLogin
from .DataManager.CookieManager import CookieManage
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment

class Login:
    def __init__(self, bot: Bot, event: GroupMessageEvent):
        self.bot = bot
        self.event = event


    async  def run(self):
        sign_in = TvLogin()
        auth_url = await sign_in.get_auth_code()
        if auth_url is None:
            await self.bot.send(self.event,"获取登录url错误，请稍后再试")
        else:
            img = await self.make_qrcode(auth_url)
            await self.bot.send(self.event, img)
            start = time.time()
            while True:
                if time.time() - start > 150:
                    message = "登录超时"
                    break
                else:
                    result = await sign_in.get_token()
                    if "code" in result and result["code"] == 0:
                        access_token = result["data"]["access_token"]
                        refresh_token = result["data"]["refresh_token"]
                        expires = result["data"]["cookie_info"]["cookies"][0]["expires"]
                        cookie = {
                            cookie_dict["name"]: cookie_dict["value"]
                            for cookie_dict in result["data"]["cookie_info"]["cookies"]
                        }
                        mid= result["data"]["mid"]
                        message = "登录成功"
                        with CookieManage() as store:
                            await store.delete_old_cookie()
                            await store.store_cookie(
                                json.dumps(cookie), access_token, refresh_token, expires,mid
                            )
                        break
                    await asyncio.sleep(5)
            await self.bot.send(self.event,message)


    async def make_qrcode(self,url):
        qr_url = url
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=1,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte = BytesIO()
        img.save(img_byte, format="PNG")
        binary_content = img_byte.getvalue()
        return MessageSegment.image(binary_content)


