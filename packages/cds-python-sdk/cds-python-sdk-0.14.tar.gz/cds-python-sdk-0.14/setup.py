# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="cds-python-sdk",
    version="0.14",
    author="capitalonline",
    description="首云python SDK",

    # 项目主页
    url="http://capitalonline.net/",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)