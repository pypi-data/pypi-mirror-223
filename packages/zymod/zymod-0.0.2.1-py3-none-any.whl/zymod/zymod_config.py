#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from happy_python.happy_config import HappyConfigBase
from happy_python.happy_exception import HappyPyException


def param_check(zy_config_value, zy_config_key):
    if zy_config_value == '':
        raise HappyPyException("配置文件中 " + zy_config_key + " 字段为空")


class LoadCustomizeZymodConfig(HappyConfigBase):
    pass


class LoadPublicZymodConfig(HappyConfigBase):
    def __init__(self):
        super().__init__()

        self.section = 'zymod'
        self.mod_name = ''
        self.active = True
        self.agent_host = ''
        self.agent_port = ''
        self.debug = 3
        self.dry_run = False
        self.interval = 0
        self.token = ''
        self.host = ''
        self.language_file = ''
        self.display_name = ''
        self.mod_type = ''
