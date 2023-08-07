import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from os import path, getcwd,listdir
import sys
sys.path.append(path.join(getcwd(),"plugins"))


nonebot.init()
nonebot.load_all_plugins(["bili_eta.plugins.eta",i for i in listdir(path.join(getcwd(),"plugins"))],[])
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
app = nonebot.get_asgi()
config = nonebot.get_driver().config

