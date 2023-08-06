# -*- coding: utf-8 -*-
# @time:   2023/2/21 9:53
# @author: Zx

import nacos
import socket
import configparser
from io import StringIO
from nacos_test.common.common import logger


def get_addr(nacos_url):
    addr, username, password = None, None, None
    # nacos_url = str(os.getenv('NACOS'))
    if nacos_url == "None":
        logger.info("nacos连接地址为None")
        return None
    if nacos_url.startswith('http://'):
        logger.debug('nacos_url1:{}'.format(nacos_url))
    else:
        nacos_url = nacos_url.split(" ")
        if len(nacos_url) > 1:
            logger.info("获取用户名密码")
            for i in nacos_url:
                if "-Dspring.cloud.nacos.server-addr=" in i:
                    addr = i.split("-Dspring.cloud.nacos.server-addr=")[1]
                if "-Dspring.cloud.nacos.username=" in i:
                    username = i.split("-Dspring.cloud.nacos.username=")[1]
                if "-Dspring.cloud.nacos.password=" in i:
                    password = i.split("-Dspring.cloud.nacos.password=")[1]
            return addr, username, password
        else:
            logger.info("获取url")
            addr = nacos_url[0].split("-Dspring.cloud.nacos.server-addr=")[1]
            return addr, username, password
    return nacos_url, username, password


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class NacosClient(object):
    def __init__(self, serving_addr=None, nacos_url=None,namespace="public"):
        if serving_addr is None:
            self.serving_addr, self.username, self.password = get_addr(nacos_url)
            if self.serving_addr is None:
                raise Exception("未读取到nacos地址！")
        else:
            self.serving_addr = serving_addr
            self.username = None
            self.password = None
        self.namespace = namespace
        self.client = nacos.NacosClient(server_addresses=self.serving_addr, namespace=self.namespace,
                                        username=self.username, password=self.password)

    def get_config(self, data_id, group="DEFAULT_GROUP"):
        event_config = self.client.get_config(data_id=data_id, group=group)
        if event_config is not None:
            event_config = "[common]\n" + event_config
        config_parser = configparser.ConfigParser()
        config_parser.read_file(StringIO(event_config))
        return config_parser

    def get_value(self, key, data_id, group="DEFAULT_GROUP"):
        config_parser = self.get_config(data_id=data_id, group=group)
        value = config_parser.get("common", key)
        return value

    def get_services(self, service_name):
        services_host = self.client.list_naming_instance(service_name)
        if services_host is not None:
            return services_host
        else:
            raise Exception("未获取到服务 %s" % service_name)

    # 注册服务
    def add_naming_instance(self, service_name, port, metdata, cluster_name="DEFAULT"):
        ip = get_host_ip()
        instance = self.client.add_naming_instance(service_name=service_name, ip=ip, port=port,
                                                   cluster_name=cluster_name, metadata=metdata)
        return instance

    # 发送心跳
    def send_heartbeat(self, service_name, port, metdata):
        ip = get_host_ip()
        heartbeat = self.client.send_heartbeat(service_name=service_name, ip=ip, port=port, metadata=metdata)
        return heartbeat


