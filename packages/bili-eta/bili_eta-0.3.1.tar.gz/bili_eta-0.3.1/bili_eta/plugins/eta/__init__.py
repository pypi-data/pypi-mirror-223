from .Command import *
from .tasks import *
from os import path, getcwd
from pathlib import Path
import nonebot
print(123)
sub_plugins = nonebot.load_plugins(str(Path(getcwd()).joinpath("plugins").resolve()))
print(345)

# import httpx
# import json
# url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all"
# headers= {
#     "cookie":"buvid3=A2F9836E-E7C3-5CBE-D18E-001E9EFC4EF397161infoc; b_nut=1672916197; i-wanna-go-back=-1; b_ut=5; _uuid=C2684D91-2102A-FD4B-1891-A21E311A56D397708infoc; buvid_fp=793b44b873c95cefd3c4cbbb4426fb45; buvid4=777D6561-DED4-5524-9C5A-4C310A1D01B398679-023010518-hpoSt0fUM%2FcVVbDh%2FCeZouRGEm6AOGjCr9geLCD2G50YhNFEcH5e5g%3D%3D; SESSDATA=f155ffa2%2C1689177253%2Cfdc42%2A12; bili_jct=f4b563f0a0083fab1b6b708413f929ae; DedeUserID=37815472; DedeUserID__ckMd5=8d9f478853b39f41; bp_video_offset_37815472=751030011778039800; LIVE_BUVID=AUTO9616729162282846; PVID=23; CURRENT_FNVAL=4048; rpdid=0zbfVFS8gq|16GNk2KpJ|22|3w1Pdo2l; hit-new-style-dyn=0; hit-dyn-v2=1; nostalgia_conf=-1; CURRENT_QUALITY=116; fingerprint=793b44b873c95cefd3c4cbbb4426fb45; buvid_fp_plain=undefined; sid=6nvxga53; innersign=0; b_lsid=10CE83B85_185B04DF4BB; _dfcaptcha=c727997e08cafa508243b64122d0c79f",
#     "referer":"https://t.bilibili.com/?spm_id_from=..0.0",
#     "origin":"https://t.bilibili.com"
# }

# result = httpx.get(url,headers=headers)

# with open("a.json","w") as f:
#     f.write(json.dumps(result.json()))


# print()

