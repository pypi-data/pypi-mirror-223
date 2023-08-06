#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2022-10-24 00:20
@Author  :   坐公交也用券
@Version :   1.1.5
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   这是一个Linux管理脚本的基础库，通过对Linux基本功能进行封装，实现快速开发的效果
"""

from .AptManage import NewAptManagement
from .Cmd import NewCommand
from .Dpkg import NewDpkgManagement
from .NewFileManagement import NewFileManagement
from .Iptables import IpTables
from .Jurisdiction import Jurisdiction
from .NmcliManger import NetManagement
from .NewNetStatus import NewNetStatus, NewNetworkCardInfo
from .OsInfo import *
from .OsInfo import OsInfo
from .Package import NewPackageManagement
from .Service import NewServiceManagement
from .Yum import YumManager
from .get import headers, cookies
from .base import list_get_len, list_remove_none
from .logger import ColorLogger

__all__ = ["NewCommand", "NewAptManagement", "NewDpkgManagement", "NewFileManagement", "Jurisdiction",
           "NetManagement", "NewNetStatus", "NewPackageManagement", "NewServiceManagement", "YumManager", "IpTables",
           "OsInfo", "NewNetworkCardInfo", "list_get_len", "list_remove_none", "ColorLogger"]

if platform.system().lower() != 'linux'.lower():
	print('Plmb模块仅支持Linux系统')
