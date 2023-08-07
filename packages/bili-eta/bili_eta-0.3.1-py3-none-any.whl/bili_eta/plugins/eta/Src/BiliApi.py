import time
from hashlib import md5
from typing import Optional, Union
from urllib.parse import urlencode

import httpx
from nonebot import logger


class TvLogin:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88\
                                      Safari/537.36 Edg/87.0.664.60",
            "Referer": "https://www.bilibili.com/",
        }
        self.local_id = 0
        self.auth_code = None
        self.app_key = "4409e2ce8ffd12b8"
        self.app_sec = "59b43e04ad6965f34319062b478f83dd"

    async def get_auth_code(self):
        """
        获取用于制作扫码登录的二维码的链接和用于查看是否扫码登录成功的auth_code
        :return:
        """

        params: dict = {
            "local_id": self.local_id,
            "appkey": self.app_key,
            "ts": int(time.time()),
        }
        params["sign"] = md5(
            f"{urlencode(sorted(params.items()))}{self.app_sec}".encode(
                "utf-8")
        ).hexdigest()
        try:
            async with httpx.AsyncClient(headers=self.headers) as session:
                url = (
                    "https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code"
                )
                response = await session.post(url, data=params)
                data = response.json()
                self.auth_code = data["data"]["auth_code"]
                logger.info("获取auth_code成功")
                return data["data"]["url"]
        except Exception as e:
            logger.exception("What?!")
            return None

    # 获取token
    async def get_token(self):

        params: dict = {
            "local_id": self.local_id,
            "appkey": self.app_key,
            "ts": int(time.time()),
            "auth_code": self.auth_code,
        }
        params["sign"] = md5(
            f"{urlencode(sorted(params.items()))}{self.app_sec}".encode(
                "utf-8")
        ).hexdigest()
        try:
            url = "https://passport.bilibili.com/x/passport-tv-login/qrcode/poll"
            async with httpx.AsyncClient(headers=self.headers) as session:
                response = await session.post(url, data=params)
                return response.json()
        except Exception as e:
            logger.error(e)

    # 刷新cookie
    async def refresh_cookie(self, access_token: str, refresh_token: str):
        params: dict = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "appkey": self.app_key,
        }
        params["sign"] = md5(
            f"{urlencode(sorted(params.items()))}{self.app_sec}".encode(
                "utf-8")
        ).hexdigest()
        try:
            url = "https://passport.bilibili.com/api/v2/oauth2/refresh_token"
            async with httpx.AsyncClient(headers=self.headers) as session:
                response = await session.post(url, data=params)
                return response.json()
        except Exception as e:
            logger.error(e)


class Api:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88\
                              Safari/537.36 Edg/87.0.664.60",
            "Referer": "https://www.bilibili.com/",
        }

    async def get_short_link(self, long_url):
        """
        获取短链接
        :param long_url:
        :return:
        """
        async with httpx.AsyncClient(headers=self.headers) as session:
            try:
                url = "https://api.bilibili.com/x/share/click"
                data = {
                    "build": "9331",
                    "buvid": "74fe03588ceace988e365fd982bd0955",
                    "oid": long_url,
                    "platform": "ios",
                    "share_channel": "COPY",
                    "share_id": "public.webview.0.0.pv",
                    "share_mode": "3",
                }
                response = await session.post(url, data=data)
                response = response.json()
                return response["data"]["content"]
            except Exception as e:
                logger.exception("What?!")
                return

    async def get_uid_info(self, uid: str) -> Optional[dict]:
        """
        :param uid:UID
        :return:
        """
        async with httpx.AsyncClient() as session:
            params = {"mid": uid, "photo": "1", "jsonp": "jsonp"}
            try:
                url = "https://api.bilibili.com/x/web-interface/card"
                response = await session.get(url, params=params, headers=self.headers)
                response = response.json()
                if response["code"] == 0:
                    return {
                        "nick_name": response["data"]["card"]["name"],
                        "roomStatus": 1,
                        "liveStatus": 0,
                    }
                return None
            except Exception as e:
                logger.exception("What?!")
                return None

    async def change_follow(
        self, uid: str, act: int, cookie: dict
    ) -> Union[str, None, bool]:
        """
        将up添加到关注列表或者从关注列表删除up
        :param uid:要关注或者取关的UID
        :param act: 1为关注，2为取关
        :param cookie:cookie
        :return:
        """
        url = "https://api.bilibili.com/x/relation/modify"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Referer": "https://space.bilibili.com",
            "referer": f"https://space.bilibili.com/{uid}?spm_id_from=..0.0",
        }
        data = {
            "fid": f"{uid}",
            "act": f"{act}",
            "re_src": "11",
            "spmid": "333.999.0.0",
            "extend_content": {"entity": "user", "entity_id": uid},
            "json": "json",
            "csrf": cookie["bili_jct"],
        }
        try:
            response = httpx.post(url=url, headers=headers,
                                  data=data, cookies=cookie)
            response = response.json()
            return True if response["code"] == 0 else response["message"]
        except Exception as e:
            logger.warning(e)
            return "添加关注错误"

    async def get_room_info(self, uid_list: list) -> Optional[dict]:
        """
        查看是否开播,以及直播间信息
        :param uid_list: UID的列表
        :return:空或者字典
        """
        uids = {"uids": uid_list}
        try:
            async with httpx.AsyncClient(headers=self.headers) as session:
                url = (
                    "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
                )
                response = await session.post(url, json=uids)
                data = response.json()
                data = data["data"]
            return data
        except Exception as e:
            logger.exception("What?!")
            return
    
    async def get_follow_list(self,uid:str,cookie:dict,page:int) -> Optional[dict]:
        headers = {
            "referer":f"https://space.bilibili.com/{uid}/fans/follow?spm_id_from=..0.0"
        }
        url = f"https://api.bilibili.com/x/relation/followings"
        params = {
            "vmid":uid,
            "pn":page,
            "ps":50
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers,cookies=cookie,params=params)
                result = response.json()
            return result["data"]["list"]
        except TimeoutError as e:
            logger.exception("error")
            return None

    async def get_location(self, url: str):
        """通过短链接获取动态链接"""
        try:
            async with httpx.AsyncClient() as client:
                url = url
                response = await client.get(url, headers=self.headers)
            return response.headers.get("location")
        except TimeoutError as e:
            logger.exception("error")
            return
    
    async def get_follow_dynamic(self,cookie):
        headers = {
            "referer":"https://t.bilibili.com/?spm_id_from=..0.0",
            "origin":"https://t.bilibili.com"
        }
        url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers,cookies=cookie)
            response = response.json()
            return response["data"]["items"]
        except Exception as e:
            logger.exception("?")
            return []
    async def get_dynamic_detail(self,dyn_id):
        url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id={dyn_id}&features=itemOpusStyle"
        headers = {
            "referer": f"https://t.bilibili.com/{dyn_id}",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient() as client:
                message =await client.get(url, headers=headers)
            if message:
                message_json = message.json()
                if message_json["code"] == 0:
                    return message_json
            return None 
        except Exception as e:
            logger.exception("?")
            return None
        
# if __name__ == '__main__':
#     auth = TvLogin()
#