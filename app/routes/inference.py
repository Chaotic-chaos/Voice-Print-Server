# -*- coding: utf-8 -*-
'''
Project:       /root/voice-print-server/app/routes
File Name:     inference.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/24
Software:      Vscode
'''

'''Main inference route'''
import io
import os
from statistics import mode
import tempfile
import time
from sanic import json, text
from sanic.views import HTTPMethodView
from sanic.log import logger
from sanic.views import stream
import pydub

class Inference(HTTPMethodView):
    # @stream
    async def post(self, request):
        '''
        1. receive a file
        2. keep it in memory
        3. inference a feature
        4. check if database has this speaker
        5. return result
        '''

        app = request.app

        logger.info("Receiving a new file, starting...")
        receive_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        # write into a file
        filename = f"{os.path.join(app.config.model['inference_folder'], receive_time)}.wav"
        # check if it is a mp3
        if request.body.startswith(b"RIFF"):
            with open(filename, "ab") as wav_file:
                # while True:
                #     chunk = await request.stream.read()
                #     if chunk is None:
                #         break
                #     wav_file.write(chunk)
                wav_file.write(request.body)
        else:
            # convert it into wav
            # save into a temp file
            temp_file = tempfile.TemporaryFile()
            temp_file.write(request.body)
            temp_file.seek(0)

            read_file = pydub.AudioSegment.from_mp3(temp_file)

            # save as a wav
            read_file.export(filename, format="wav")

        recognition_res = await app.ctx.model.recognition(filename)

        complete_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

        logger.info(f"Finished with file {filename}, details is {recognition_res}, returning result...")

        try:
            hit = [speaker for speaker, probility in recognition_res.items() if probility > app.config.model["threshold"]][0]
        except Exception as e:
            hit = None
        return json({
            "time": {
                "start": receive_time,
                "complete": complete_time,
            },
            "hit": hit,
            "detailes": {speaker: str(recognition_res[speaker]) for speaker in recognition_res.keys()}
        })
