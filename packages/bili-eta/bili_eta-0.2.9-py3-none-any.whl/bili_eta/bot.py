
import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()
nonebot.load_plugin("bili_eta.plugins.eta")
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
app = nonebot.get_asgi()
config = nonebot.get_driver().config
print(nonebot.get_plugin_by_module_name())
# def run():
#     nonebot.run(app=app)
