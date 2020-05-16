#!/usr/bin/env python3
# - *- coding: utf- 8 - *-
import requests
import json

# GET REQUEST - VERI ÇEKME
def getData(url):
    istek = requests.get(url)
    return istek.json()

# DELETE REQUEST - VERI SİLME
def deleteData(url):
    requests.delete(url)

# POST DATA - YENI VERI EKLEME
def postData(url, payload):
    headers = {'content-type': 'application/json'}
    istek = requests.post(url, data=json.dumps(payload), headers=headers)

# PUT DATA - VERI DEĞİŞTİRME
def putData(url, payload):
    print('putData() '+json.dumps(payload))
    headers = {'content-type': 'application/json'}
    istek = requests.put(url, data=json.dumps(payload), headers=headers)