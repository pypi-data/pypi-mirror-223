# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-31 16:21:27
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:39:22
from typing import List


class PluginSuiteSetObj:
    def __init__(self, plugins) -> None:
        self.data = plugins

    def get_data(self) -> List[str]:
        return self.data
