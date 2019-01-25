# coding=utf-8
import gevent.monkey
gevent.monkey.patch_all()

debug = True
loglevel = 'debug'
bind = "0.0.0.0:8800"
daemon = False

# 启动的进程数
workers = 2
worker_class = 'gevent'