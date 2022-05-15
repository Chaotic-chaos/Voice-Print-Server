# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server/app/utils
File Name:     config.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''

import yaml


class ServerConfig():
    def __init__(self, config_path) -> None:
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

    def __call__(self, *args, **kwds):
        return self._config
