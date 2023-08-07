import os
import sqlite3
from typing import Optional, Union


class FollowManage:
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

    

    async def get_follow_by_uid(self,uid:str) -> tuple:
        """查看本地的关注列表内是否关注了此uid

        Parameters
        ----------
        uid : str
            uid
        """

        sql = "select UID,Name from FollowerReserve where UID=?"
        data = (uid,)
        self.cursor.execute(sql,data)
        return self.cursor.fetchone()
    
    async def store_follow_info(self,uid:str,uname:str):
        """存储关注信息

        Parameters
        ----------
        uid : str
            uid
        uname : str
            用户名
        """
        add_sql = "insert into FollowerReserve (UID,Name) values(?,?);"
        data = (uid,uname,)
        self.cursor.execute(add_sql, data)
    
    async def delete_follow(self,uid:str):
        """删除关注列表的信息

        Parameters
        ----------
        uid : str
            uid
        """
        del_sql = "delete from FollowerReserve where UID=?"
        data = (uid,)
        self.cursor.execute(del_sql,data)


    async def del_all_follow(self):
        """删除关注列表内的所有的信息
        """
        del_sql = "delete from FollowerReserve"
        self.cursor.execute(del_sql)

if __name__ == "__main__":
    import asyncio
    async def run():
        with FollowManage() as d:
            result = await d.get_follow_by_uid("2049968320")
        print(result)

    asyncio.run(run())