
import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()
nonebot.load_plugins("./plugins")
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
app = nonebot.get_asgi()
config = nonebot.get_driver().config

# def run():
#     nonebot.run(app=app)