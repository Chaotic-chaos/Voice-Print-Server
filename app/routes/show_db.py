# -*- coding: utf-8 -*-
'''
Project:       /root/voice-print-server/app/routes
File Name:     show_db.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/24
Software:      Vscode
'''

'''
Show all registered speakers
'''

import os
import time
from sanic import json
from sanic.views import HTTPMethodView
from sanic.log import logger

class ShowRegistered(HTTPMethodView):
    async def get(self, request):
        app = request.app

        logger.info("Showing all registered speakers...")
        start_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        register_speakers = [name.split(".")[0] for name in os.listdir(app.config.model["audio_db_path"])]

        complete_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        return json({
            "time": {
                "start": start_time,
                "complete": complete_time
            },
            "speakers": register_speakers
        })