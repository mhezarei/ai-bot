#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 10:55:00 2020

@author: mahsa
"""

import datetime
import json

import requests as rq


class Deepmine():
    def __init__(self):
        self.start = datetime.datetime.now()
        self.token = self.get_token()
        
    def get_token(self):
        data = {
      'grant_type': '',
      'username': 'aibot',
      'password': 'aibot-user@deepmine.ir'
    }
        try:
            response = rq.post('https://deepmine.ir:8095/token', data=data, verify=False)
        except Exception:
            return 0
        token = json.loads(response.content)['access_token']
        return token
    
    def refresh_token(self):
        if (datetime.datetime.now()-self.start).seconds > 3599 :
            self.start = datetime.datetime.now()
            self.token = self.get_token()
    
    def get_text(self,file_path):
        self.refresh_token()
        if self.token == 0 :
            return 0,"Error in get_token from Deepmine"
        headers = {
    'Authorization': 'Bearer '+self.token
    }

        params = (
        ('nbest', '1'),
        )
    
        files = {
        'file': (file_path, open(file_path, 'rb')),
        }
    
        response = rq.post('https://deepmine.ir:8095/file2text', headers=headers, params=params, files=files, verify=False)
        if response.status_code == 200:
            try:
                text = json.loads(response.content)['data'][0]['text']
                return 1,text
            except Exception as e:
                return 0,e
                
        else:
            return 0,response.content



