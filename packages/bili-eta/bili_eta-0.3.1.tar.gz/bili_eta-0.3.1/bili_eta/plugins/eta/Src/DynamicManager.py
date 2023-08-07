# from bilirpc.api import get_space_dynamic,get_follow_dynamic
from .BiliApi import  Api
from .DataManager import DataManage
import json
from google.protobuf.json_format import MessageToJson
from .StatuChecker import Check

class DynamicManage:
    def __init__(self) -> None:
        self.api = Api()

    async def refresh_dynamic_id(self):
        ck = Check()
        cookies =await ck.check_login()
        if cookies:
            token = cookies["cookie"]
            all_dynamic = await self.api.get_follow_dynamic(token)
            if all_dynamic:
                with DataManage() as ck:
                    all_dynamic_id = await ck.acquire_all_dynamic_id()
                    for item in all_dynamic:
                        dyn_id = item["id_str"]
                        uid = item["modules"]["module_author"]["mid"]
                        uname = item["modules"]["module_author"]["name"]
                        if dyn_id not in all_dynamic_id:
                            await ck.store_dynamic_id(dyn_id,uname,json.dumps(item),uid,"web")

    





        

