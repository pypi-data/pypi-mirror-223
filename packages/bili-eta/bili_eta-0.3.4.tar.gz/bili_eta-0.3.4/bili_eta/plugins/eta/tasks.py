from nonebot import require
from .Src.DynPusher import DynPush
from .Src.LivePusher import LivePush

scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job('cron', second='*/6', id='dynamic_push', max_instances=10)
async def _():
    await DynPush().run()


@scheduler.scheduled_job('cron', second='*/10', id='live_push', max_instances=10)
async def _():
    await LivePush().run()