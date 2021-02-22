#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:29:02 2021

@author: mahsa
"""


import json

import requests as req


def aryana(text):
    body = {
        "Text": text,
        "Speaker": "Female1",
        "PitchLevel": "4",
        "PunctuationLevel": "2",
        "SpeechSpeedLevel": "5",
        "ToneLevel": "10",
        "GainLevel": "3",
        "BeginningSilence": "0",
        "EndingSilence": "0",
        "Format": "wav16",
        "Base64Encode": "0",
        "Quality": "normal",
        "APIKey": "0IYTIY5JNLOU8ON"
    }
    header = {"Content-type": "application/json"}
    r = req.post("http://api.farsireader.com/ArianaCloudService/ReadText",
                 headers=header, data=json.dumps(body), timeout=10)
    return r


if __name__ == '__main__':
    """
    START

    """
    text = ""
    resp = aryana(text)
    file = "path/to/wav/file.wav"
    with open(file, mode='bx') as f:
        f.write(resp.content)
