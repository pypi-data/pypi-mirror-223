import os
import sqlite3
from typing import Optional


class SwitchManage:
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




    async def store_SwitchStatus(self, switch_position: str, bot_id: int) -> None:
        """
        将bot开关存入数据库
        :param switch_type: str
        :param switch_position:int
        :param bot_id: int
        :return: None
        """
        store_sql = "insert into BotSwitch (SwitchPosition,BotId) values(?,?);"
        data = (
            switch_position,
            bot_id,
        )
        self.cursor.execute(store_sql, data)

    async def del_SwitchStatus(self, switch_position: str, bot_id: int) -> None:
        del_sql = "delete from SubInfoReserve where SwitchPosition=? and BotId=?"
        data = (
            switch_position,
            bot_id,
        )
        self.cursor.execute(del_sql, data)

    async def acquire_SwitchStatus(self, group_id: str, bot_id: int) -> Optional[tuple]:
        """
        通过群号查找对应群机器人的开关状态
        :param group_id: str
        :param bot_id: int
        :return: Optional[tuple[int]]
        """
        acquire_sql = (
            "select SwitchStatus from BotSwitch where  SwitchPosition=? and BotId=?"
        )
        data = (
            group_id,
            bot_id,
        )
        return self.cursor.execute(acquire_sql, data).fetchone()

    async def modify_SwitchStatus(
        self, switch_position: str, bot_id: int, status: int
    ) -> None:
        """
        修改Bot开关状态
        :param status:
        :param switch_position:
        :param bot_id:
        :return:
        """
        modify_sql = (
            "update BotSwitch set SwitchStatus = ? where SwitchPosition=? and BotId=?"
        )
        data = (
            status,
            switch_position,
            bot_id,
        )
        self.cursor.execute(modify_sql, data)