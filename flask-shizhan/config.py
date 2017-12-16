# encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)


DIALECT = 'postgresql'
# 驱动
DRIVER = ''
# 用户名
USERNAME = 'postgres'
# 密码
PASSWORD = 'wudong510015'
# 服务器地址
HOST = 'localhost'
# 端口号，在数据库中可以设置
PORT = '5432'
# 数据库名称
DATABASE = 'DEMO_shizhan'
# 连接数据库
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(DIALECT, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
