import os
import sqlite3
from typing import Union


class DataManage:
    def __enter__(self):
        database_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "SubData.db"
        )
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        # 如果不存在则创建一个存Cookie的表
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS CookieReserve 
                                (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                Cookie  TEXT  NOT NULL,
                                AccessToken TEXT NOT NULL,
                                RefreshToken TEXT NOT NULL,
                                Expires INT  NOT NULL,
                                Mid TEXT NOT NULL);"""
        )

        # 如果不存在则创建一个存订阅信息的表
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS SubInfoReserve 
                                (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                UID  TEXT  NOT NULL,
                                Name TEXT NOT NULL,
                                LiveStatus  INT  NOT NULL,
                                Bot TEXT NOT NULL,
                                Position TEXT NOT NULL,
                                PositionType TEXT NOT NULL,
                                DynamicOn INT NOT NULL DEFAULT 1,
                                LiveOn INT NOT NULL DEFAULT 1);"""
        )

        # 如果不存在就创建一个存bot开关的表
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS BotSwitch 
                                (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                SwitchPosition TEXT NOT NULL,
                                SwitchStatus  INT  NOT NULL DEFAULT 1,
                                BotId TEXT INT NULL );"""
        )

        # 如果不存在就创建一个存动态的ID以及动态内容以及发动态的人的表
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS DynamicReserve 
                                (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                Name   TEXT NOT NULL,
                                UID     TEXT NOT NULL,
                                DynType TEXT NOT NULL,
                                Dynamic TEXT NOT NULL,
                                DynamicText TEXT NOT NULL
                                );"""
        )

        # 如果不存在就创建一个存关注列表的表
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS FollowerReserve 
                                (ID INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                UID TEXT NOT NULL,    
                                Name   TEXT NOT NULL
                                );"""
        )


        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    async def store_sub_info(
        self,
        uid: str,
        name: str,
        live_status: int,
        sub_group: str,
        bot_id: str,
        position_type: str,
        live_on: int = 1,
        dynamic_on: int = 1,
    ) -> None:
        """
        新增加订阅数据到数据库中
        :param position_type:订阅位置的类型 group | guild
        :param dynamic_on:是否开启动态推送
        :param live_on:是否开启直播推送
        :param bot_id:bot的id
        :param uid:订阅的uid
        :param name: 昵称
        :param live_status:直播状态
        :param sub_group: 订阅的群或者频道
        :return: None
        """
        store_sql = (
            "insert into SubInfoReserve (UID,Name,LiveStatus,Position,Bot,PositionType,DynamicOn,"
            "LiveOn) values(?,?,?,?,?,?,?,?); "
        )
        data = (
            uid,
            name,
            live_status,
            sub_group,
            bot_id,
            position_type,
            dynamic_on,
            live_on,
        )
        self.cursor.execute(store_sql, data)

    async def del_sub_info_by_uid(self, uid: str, bot: str, position: str):
        del_sql = "delete from SubInfoReserve where UID=? and Position=? and Bot=?"
        data = (
            uid,
            position,
            bot,
        )
        self.cursor.execute(del_sql, data)
    
    async def del_all_sub_by_uid(self,uid:str):
        del_sql = "delete from SubInfoReserve where UID=?"
        data= (uid,)
        self.cursor.execute(del_sql, data)

    async def modify_live_on(self, uid: str, bot: str, position: str, act: int):
        modify_sql = (
            "update SubInfoReserve set LiveOn = ? where UID=? and Bot=? and Position=?"
        )
        data = (
            act,
            uid,
            bot,
            position,
        )
        self.cursor.execute(modify_sql, data)

    async def modify_dynamic_on(self, uid: str, bot: str, position: str, act: int):
        modify_sql = "update SubInfoReserve set DynamicOn = ? where UID=? and Bot=? and Position=?"
        data = (
            act,
            uid,
            bot,
            position,
        )
        self.cursor.execute(modify_sql, data)

    async def modify_live_status(self, uid: str, live_status: int) -> None:
        modify_sql = "update SubInfoReserve set LiveStatus = ? where UID=?"
        data = (
            live_status,
            uid,
        )
        self.cursor.execute(modify_sql, data)

    async def acquire_sub_info_by_uid(
        self, uid: str, position: str, bot: str
    ) -> Union[tuple, None]:
        """
        通过uid查找订阅信息
        :param bot:
        :param position:
        :param uid:
        :return:
        """
        acquire_sql = "select UID,Name,LiveStatus,LiveOn,DynamicOn from SubInfoReserve where UID = ? and Bot=? and Position=?"
        data = (
            uid,
            bot,
            position,
        )
        return self.cursor.execute(acquire_sql, data).fetchone()

    async def acquire_full_sub_info(self) -> Union[list, None]:
        """
        获取所有信息
        :return: Union[tuple, None]
        """
        self.cursor.execute("select UID,Name,LiveStatus,Position from SubInfoReserve")
        return self.cursor.fetchall()

    async def acquire_sub_info_by_position(self, bot: str, position: str):
        acquire_sql = "select UID,Name,LiveStatus,LiveOn,DynamicOn from SubInfoReserve where  Bot=? and Position=?"
        data = (bot, position)
        return self.cursor.execute(acquire_sql, data).fetchall()

    async def store_dynamic_id(self, dynamic_id: str, name:str,dynamic_json:str,uid:str,dyn_type:str) -> None:
        """将动态ID、动态文本以及发表动态的人的ID记录到表中

        Args:
            dynamic_id (str): 动态ID
            name (str): 发送动态的人的ID
            dynamic_json (str): 动态的json数据（经过了json库的dump）
        """

        store_sql = "insert into DynamicReserve (Name,Dynamic,DynamicText,UID,DynType) values(?,?,?,?,?);"
        data = (name,dynamic_id,dynamic_json,uid,dyn_type,)
        self.cursor.execute(store_sql, data)

    async def acquire_dynamic_id(self, dynamic_id: str) -> Union[None, tuple]:
        """查找特定的动态ID
        Args:
            dynamic_id (str): 动态的ID

        Returns:
            Union[None, tuple]: 含有动态ID的元组
        """
        acquire_sql = "select Dynamic from DynamicReserve where Dynamic = ?"
        data = (dynamic_id,)
        return self.cursor.execute(acquire_sql, data).fetchone()
    
    async def acquire_all_dynamic_id(self) -> Union[None, tuple]:
        acquire_sql = "select Dynamic from DynamicReserve"
        return self.cursor.execute(acquire_sql).fetchall()

    async def acquire_dynamic_by_dyn_id(self,dyn_id):
        acquire_sql = "select UID,DynType,Dynamic,DynamicText from DynamicReserve where Dynamic = ?"
        data = (dyn_id,)
        self.cursor.execute(acquire_sql,data)
        return self.cursor.fetchone()
        
    async def acquire_dynamic_by_uid(self,uid):
        acquire_sql = "select UID,DynType,Dynamic,DynamicText from DynamicReserve where UID = ?"
        data = (uid,)
        self.cursor.execute(acquire_sql,data)
        return self.cursor.fetchone()


    async def acquire_dynamic_id_num(self) -> tuple:
        """查看表中的存储的动态是否为空

        Returns:
            tuple: 返回的动态的数量
        """
        acquire_sql = "SELECT count(Dynamic) FROM DynamicReserve"
        return self.cursor.execute(acquire_sql).fetchone()

    async def del_sub_info_by_position(self, bot: str, position: str) ->None:
        """退群时根据退群的bot的id和推出的群的群号删除所有订阅
        Args:
            bot (str): 退群的bot的id    
            position (str): 所退的群
        """
        sql = "delete from SubInfoReserve where Bot=? and Position=?"
        data = (
            bot,
            position,
        )
        self.cursor.execute(sql, data)

    async def acquire_live_push_uid(self) -> Union[None,list]:
        """查找开启了直播推送并且机器人开关开了的订阅的uid

        Returns:
            Union[None,list]: 返回值
        """
        sql = (
            "SELECT DISTINCT s.UID FROM SubInfoReserve AS s INNER JOIN BotSwitch AS b WHERE s.Position = b.SwitchPosition "
            "and b.SwitchStatus=1 AND s.LiveOn=1 GROUP BY s.UID "
        )
        return self.cursor.execute(sql).fetchall()

    async def acquire_live_status(self, uid: str) -> tuple:
        sql = "SELECT LiveStatus FROM SubInfoReserve WHERE UID=? GROUP BY UID"
        data = (uid,)
        return self.cursor.execute(sql, data).fetchone()

    async def acquire_live_push_info_by_uid(self, uid: str) ->list:
        sql = (
            "SELECT DISTINCT s.Bot,s.Position,s.PositionType FROM SubInfoReserve AS s INNER JOIN BotSwitch AS b WHERE "
            "s.UID=? AND b.SwitchPosition = s.Position and s.Bot=b.BotId and b.SwitchStatus=1 and s.LiveOn=1; "
        )
        data = (uid,)
        return self.cursor.execute(sql, data).fetchall()

    async def acquire_dynamic_push_uid_all(self):
        sql = "SELECT DISTINCT s.UID, s.Name  FROM SubInfoReserve AS s INNER JOIN BotSwitch AS b WHERE b.SwitchPosition = s.Position and  s.Bot =b.BotId and b.SwitchStatus=1 and s.DynamicOn=1;"
        return self.cursor.execute(sql).fetchall()
    
    async def acquire_dynamic_push_info_by_uid(self, uid: str):
        sql = (
            "SELECT DISTINCT s.Name,s.Bot,s.Position,s.PositionType FROM SubInfoReserve AS s INNER JOIN BotSwitch AS b WHERE "
            "s.UID=? AND b.SwitchPosition = s.Position and s.Bot=b.BotId and b.SwitchStatus=1 and s.DynamicOn=1; "
        )
        data = (uid,)
        return self.cursor.execute(sql, data).fetchall()

    async def modify_name(self, uid: str, name: str):
        modify_sql = "update SubInfoReserve set Name = ? where UID=?"
        data = (
            name,
            uid,
        )
        self.cursor.execute(modify_sql, data)


if __name__ == "__main__":
    import asyncio
    async def run():
        with DataManage() as d:
            result = await d.acquire_full_sub_info()

    asyncio.run(run())