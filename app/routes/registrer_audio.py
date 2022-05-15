# -*- coding: utf-8 -*-
'''
Project:       /root/voice-print-server/app/routes
File Name:     registrer_audio.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/24
Software:      Vscode
'''

'''
Register an uploaded audio into database && file
'''
import os
import tempfile
from sanic import json
from sanic.views import HTTPMethodView
from sanic.log import logger
import time
import pydub

class RegisterAudio(HTTPMethodView):
    async def post(self, request):
        app = request.app

        logger.info("Receiving an audio, register it into database")

        start_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        # save it into file 'speaker.wav' and app.ctx.model.audio_db
        speaker = request.form["speaker"][0]

        filename = f"{os.path.join(app.config.model['audio_db_path'], speaker)}.wav"

        if request.files["audio"][0].body.startswith(b"RIFF"):
            with open(filename, "wb") as f:
                f.write(request.files["audio"][0].body)
        else:
            temp_file = tempfile.TemporaryFile()
            temp_file.write(request.files["audio"][0].body)
            temp_file.seek(0)

            read_file = pydub.AudioSegment.from_mp3(temp_file)
            read_file.export(filename, format="wav")

        await app.ctx.model.register(filename, speaker)

        complete_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        logger.info("Registered a speaker.")

        registered_speakers = [name.split(".")[0] for name in os.listdir(app.config.model["audio_db_path"])]

        return json({
            "time": {
                "start": start_time,
                "complete": complete_time
            },
            "speakers": registered_speakers
        })
