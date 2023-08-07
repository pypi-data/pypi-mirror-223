import os
import sqlite3
from typing import Optional

class CookieManage:
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



    async def store_cookie(
        self, cookie: str, access_token: str, refresh_token: str, expires: int,mid:str
    ) -> None:
        """
        将cookie存入数据库
        :param cookie: cookie
        :param access_token:
        :param refresh_token:
        :param expires:
        :return:
        """
        add_sql = "insert into CookieReserve (Cookie,AccessToken,RefreshToken,Expires,Mid) values(?,?,?,?,?);"
        data = (
            cookie,
            access_token,
            refresh_token,
            expires,
            mid
        )
        self.cursor.execute(add_sql, data)

    async def delete_old_cookie(self) -> None:
        """
        删除旧的cookie
        :return:
        """
        del_sql = "delete from CookieReserve"
        self.cursor.execute(del_sql)

    async def acquire_cookie(self) -> Optional[tuple]:
        """
        从数据库中取出 mid,AccessToken,RefreshToken,Cookie,expires
        Returns:
            Optional[tuple]: (mid:int,AccessToken:str,RefreshToken:str, Cookie:str, expires:int)
        """

        acquire_sql = "select Cookie,AccessToken,RefreshToken,Expires,Mid from CookieReserve"
        self.cursor.execute(acquire_sql)
        return self.cursor.fetchone()