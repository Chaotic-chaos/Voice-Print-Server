# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server/app/routes
File Name:     hello.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''

'''Default route'''
from sanic import text
from sanic.views import HTTPMethodView
from sanic.log import logger

class Hello(HTTPMethodView):
    async def get(self, request):
        app = request.app

        return text("<h3>Hello, welcome to voice_print_recognizer!</h3>")
