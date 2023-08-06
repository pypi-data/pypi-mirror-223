# -*- coding: utf-8 -*-

import logging


def get_logger(name):
    formatter = logging.Formatter(
        fmt='''%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s''')
    sh = logging.StreamHandler()  # 创建屏幕输出handler
    sh.setFormatter(formatter)  # 设置handler输出格式
    sh.setLevel(logging.INFO)  # 设置handler输出等级
    _log = logging.getLogger(name)  # 创建名为name值的logger
    _log.propagate = False
    _log.setLevel(logging.INFO)

    # 下面这句话是日志重复的关键
    # 1.我们想为这个logger设置不一样的输出格式，所以添加了一个屏幕输出handler
    # 2.没有设置logger的propagate值为False（默认是True），于是依据logging包官方的注释，日志记录会向上传播到他的父节点也就是root logger
    # 3.当root logger 同时也被添加了屏幕输出handler的情况，日志就会输出第二次
    # 4.解决方案有两个：一个是去掉root logger的屏幕输出handler，另一个是取消 子logger的 向上传播记录，也就是propagate值设为False
    _log.addHandler(sh)

    return _log


logger = get_logger('myApp')
