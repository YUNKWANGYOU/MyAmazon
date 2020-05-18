import pymysql
from myprogram import MyProgram

conn = pymysql.connect("localhost", user="root", password="dgu1234!", db="dgu")
a = MyProgram(conn)
a.execute()
