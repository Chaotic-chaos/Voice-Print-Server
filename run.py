# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server
File Name:     run.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''


'''Main entry of this sanic instance'''

import app

if __name__ == '__main__':
    app = app.create_app("config.yaml")

    app.run(host="0.0.0.0", port=3335, debug=app.config.get("debug", False), workers=app.config.get("WORKERS", 1))