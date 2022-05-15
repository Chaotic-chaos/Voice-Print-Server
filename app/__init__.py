# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server/app
File Name:     __init__.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''

from app.routes.inference import Inference
from app.routes.registrer_audio import RegisterAudio
from app.routes.show_db import ShowRegistered
from .utils.config import ServerConfig
import sanic
from .utils.logger import setup_logger
from .utils.model import VoicePrintModel
from .routes.hello import Hello
from sanic_cors import CORS

'''Init the whole app'''

def create_app(config_path="./config.yaml"):
    # read config
    config = ServerConfig(config_path)

    # init app
    app = sanic.Sanic(__name__)

    # solve CORS
    CORS(app)

    # update config
    app.config.update(config())

    # add handlers
    app.register_listener(setup_logger, "before_server_start")
    voice_print_model = VoicePrintModel()
    app.ctx.model = voice_print_model
    app.register_listener(voice_print_model.init_model, "before_server_start")
    app.register_listener(voice_print_model.load_audio_db, "before_server_start")

    # add routes
    app.add_route(Hello.as_view(), "/")
    app.add_route(Inference.as_view(), "/check")
    app.add_route(RegisterAudio.as_view(), "/register")
    app.add_route(ShowRegistered.as_view(), "/show")

    return app
