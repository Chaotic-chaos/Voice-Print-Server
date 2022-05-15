# -*- coding: utf-8 -*-
'''
Project:       /root/data/projects/VoiceprintRecognition-Pytorch/voice-print-server/app/utils
File Name:     model.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/04/23
Software:      Vscode
'''

'''Initiate the model instance'''

import os
from sanic.log import logger
import torch
import numpy as np
import librosa

class VoicePrintModel():
    def __init__(self) -> None:
        self.audio_db = {}
        self.model_path = None
        self.device = None
        self.threshold = None
        self.input_shape = None
        self.model = None

    async def init_model(self, app, loop):
        logger.info("Fireuping the model...")

        self.model_path = app.config.model["model_path"]
        self.device = torch.device(app.config.model["device"])
        self.threshold = app.config.model["threshold"]
        self.input_shape = app.config.model["input_shape"]

        self.model = torch.jit.load(self.model_path).eval().to(self.device)

        logger.info("Model initiated successfully!")

    async def load_audio_db(self, app, loop):
        '''
        load all the audio samples(aka registered speaker)
        '''
        logger.info("Loading all registered speakers... It going to take a while...")

        audios = os.listdir(app.config.model["audio_db_path"])


        for audio in audios:
            speaker = audio[:-4]       # xxx.wav
            try:
                feature = self._infer(os.path.join(app.config.model["audio_db_path"], audio))[0]
            except Exception as e:
                if e == AssertionError:
                    logger.warning(f"{speaker}: {audio} is illegal, skip it.")
                    continue
            self.audio_db[speaker] = feature
            logger.info(f"{speaker}: {audio} loaded successfully!")
        
        logger.info("Speaker database initiated.")

    async def recognition(self, audio):
        feature = self._infer(audio)[0]

        res = {}
        for speaker, db_feature in self.audio_db.items():
            res[speaker] = np.dot(feature, db_feature) / (np.linalg.norm(feature) * np.linalg.norm(db_feature))
            # probility = np.dot(feature, db_feature) / (np.linalg.norm(feature) * np.linalg.norm(db_feature))
        return res

    async def register(self, audio, speaker):
        logger.info(f"Registering {speaker}")
        feature = self._infer(audio)[0]
        self.audio_db[speaker] = feature
        logger.info(f"{speaker} registered successfully!")

    def _infer(self, audio_path):
        input_shape = eval(self.input_shape)
        data = self._load_audio(audio_path, mode='infer', spec_len=input_shape[2])
        data = data[np.newaxis, :]
        data = torch.tensor(data, dtype=torch.float32, device=self.device)
        # 执行预测
        feature = self.model(data)
        return feature.data.cpu().numpy()

    # 加载并预处理音频
    def _load_audio(self, audio_path, mode='train', win_length=400, sr=16000, hop_length=160, n_fft=512, spec_len=257):
        # 读取音频数据
        wav, sr_ret = librosa.load(audio_path, sr=sr)
        # 数据拼接
        if mode == 'train':
            extended_wav = np.append(wav, wav)
            if np.random.random() < 0.3:
                extended_wav = extended_wav[::-1]
        else:
            extended_wav = np.append(wav, wav[::-1])
        # 计算短时傅里叶变换
        linear = librosa.stft(extended_wav, n_fft=n_fft, win_length=win_length, hop_length=hop_length)
        mag, _ = librosa.magphase(linear)
        freq, freq_time = mag.shape
        assert freq_time >= spec_len, f"非静音部分长度不能低于1.3s, {audio_path}"
        if mode == 'train':
            # 随机裁剪
            rand_time = np.random.randint(0, freq_time - spec_len)
            spec_mag = mag[:, rand_time:rand_time + spec_len]
        else:
            spec_mag = mag[:, :spec_len]
        mean = np.mean(spec_mag, 0, keepdims=True)
        std = np.std(spec_mag, 0, keepdims=True)
        spec_mag = (spec_mag - mean) / (std + 1e-5)
        spec_mag = spec_mag[np.newaxis, :]
        return spec_mag
