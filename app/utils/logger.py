# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server/app/utils
File Name:     logger.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''
import logging
import os
from sanic.log import logger

'''Setup logger handlers'''

async def setup_logger(app, loop):
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    stream_handler = logging.StreamHandler()
    rotating_handler = logging.handlers.RotatingFileHandler(
        filename=app.config.log["filename"],
        maxBytes=app.config.log["maxBytes"],
        backupCount=app.config.log["backupCount"]
    )

    stream_handler.setLevel(level=level_map[app.config.log["level"]])
    rotating_handler.setLevel(level=level_map[app.config.log["level"]])

    stream_handler.setFormatter(logging.Formatter(app.config.log["format"]))
    rotating_handler.setFormatter(logging.Formatter(app.config.log["format"]))

    # logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)
