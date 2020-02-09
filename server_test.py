# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:45:28 2020

@author: azumi
"""

import requests


def send():
    response = requests.post('http://192.168.0.2:50000/show', 
                             data={'user': 'az',
                                   'pass': 'ma'})
    #print(response.status_code)    # HTTPのステータスコード取得
    #print(response.text)    # レスポンスのHTMLを文字列で取得
    return response
i = 0
while(True):
    i += 1
    print(i)
    response = send()
