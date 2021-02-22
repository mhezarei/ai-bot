#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:36:27 2021

@author: mahsa
"""
import asyncio
import json
import re

import requests as req
import websockets


async def send_file_nevisa(file,ip,size,name,comment):
   headers = {"subject": "SOF",
               "file-size": size,
               "file-name": name,
               "source-ip": ip,
               "settings": {"autostart": "true", "comment": comment}
               }
   endmsg = {
        "subject": "EOF"
   }
   streamBlockSize = 43967
   try:
       async with websockets.connect('ws://80.210.37.8:8087/queueFile') as ws:
           try:
                await ws.send(json.dumps(headers))
           except:
                print("Error in sending SOF message")
           try:
                re =  await ws.recv()
                re = json.loads(re)
                if re['result'] == 0:
                    try:
                        chunks = [file[i:i + streamBlockSize] for i in range(0, len(file), streamBlockSize)]
                        for chunk in chunks:
                            await ws.send(chunk)
                        await ws.send(json.dumps(endmsg))
                        re = await ws.recv()
                        re = json.loads(re)
                        if re['result'] == 0:
                            await ws.close()
                            return 1
                        else:
                            print("unsuccessfully converted file")
                            return 0
                    except:
                        print("Error in sending File")
                        return 0
                else:
                    print("Error in connecting to Nevisa,Result is not 0")
                    return 0
           except:
               print("Error in Receiving Response of SOF")
               return 0
   except:
       print("Error in connecting to Nevisa")
       return 0

def send_req_nevisa(type,uid):
    if type == "GetList":
        try:
            r = req.get("http://80.210.37.8:8087/FileAsrServlet?subject="+type,auth=req.auth.HTTPBasicAuth('ali', '123'))
        except:
            print("Request Error")
            return 0
    else:
        try:
            r = req.get("http://80.210.37.8:8087/FileAsrServlet?subject=" + type + "&uid=" + uid,auth=req.auth.HTTPBasicAuth('ali', '123'))
        except:
            print("Request Error")
            return 0
    return json.loads(r.text)

def get_uid(JFile,name,comment,ip):
    file_list = JFile['list']
    for i in file_list.keys():
        if file_list[i]['comment'] == comment and file_list[i]['fname'] == name and file_list[i]['source-ip'] == ip :
            return i

def remove_signs(text):
    while text.find(")") != -1:
        text = re.sub(r'\(([^()]*)\)','',text)
    return text

def nevisa(file,comment,ip="172.0.0.0"):
    size = str(file.__sizeof__())
    file_1 = file.read()
    name=file.name
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(send_file_nevisa(file_1,ip,size,name,comment))
    asyncio.get_event_loop().run_until_complete(send_file_nevisa(file_1,ip,size,name,comment))
    JFile = send_req_nevisa("GetList","")
    uid = get_uid(JFile,name,comment,ip)
    try:
        text = send_req_nevisa("GetText",uid)['text']
        text = remove_signs(text)
        send_req_nevisa("DeleteFile", uid)
        return text
    except Exception as e:
        print(e)
        return 0
    return 0


"""
START

"""
# file=open("{path/to/file/file.wav}",mode='rb')
# comment="{your national code}"
# text = nevisa(file,comment)
