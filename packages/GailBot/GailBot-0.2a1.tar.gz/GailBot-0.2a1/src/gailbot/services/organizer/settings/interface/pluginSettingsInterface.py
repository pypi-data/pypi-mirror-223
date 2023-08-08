# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-07-24 14:19:29
from typing import List, Dict


class PluginSettingsInterface:
    """
    Interface for plugin settings
    """

    def __init__(self, plugins: List[str]):
        self.plugins = plugins

    def get_data(self):
        """
        Accesses and returns and object's plugin settings
        """
        return self.plugins
