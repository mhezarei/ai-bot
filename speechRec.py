#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:49:51 2020

@author: mahsa
"""


import speech_recognition as sr


def google(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        data = r.record(source)
    text = r.recognize_google(data, language='fa-IR')
    return(text)