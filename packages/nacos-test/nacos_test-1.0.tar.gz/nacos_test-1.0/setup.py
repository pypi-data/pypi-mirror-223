# -*- coding: utf-8 -*-
# @time:   2023/8/4 10:05
# @author: Zx

from setuptools import setup, find_packages

setup(
    name="nacos_test",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            'nacos-sdk-python==0.1.6'
        ]
)
