# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:30 2019

@author: azumi
"""

import mysql.connector
import datetime
import pandas as pd

user_dic={'azumi':'mamiya',
           'kenshin':'kenshin',
           'daiki':'miyagawa',
           'tomohiro':'tsuchiya'}

def kakunin(user_name,user_pass,port,host,db_name):
    connected=False
    if user_pass==user_dic[user_name]:
        connected=True
    return connected

def sql_data_send(user_name,user_pass,port,host,db_name,weight_after,weight_before,contents,time,moisture,tenki,shitsudo):
    if user_pass==user_dic[user_name]:
        df = pd.read_csv('data_'+user_name+'.csv', index_col=0)
        tmp_day=datetime.date.today()
        day=tmp_day.strftime('%Y-%m-%d')
        #df.append(day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo)
        columns = ["day","weight_after","weight_before","contents","time","moisture","tenki","shitsudo"]
        tmp_se = pd.Series([day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo], index=columns, name=str(df.shape[0]))
        df = df.append(tmp_se)
        #print(df.head())
        df.to_csv('data_'+user_name+'.csv')
    return  'OK'

def sql_data_get(user_name,user_pass,port,host,db_name):
    data_list=[]
    if user_pass==user_dic[user_name]:
        df = pd.read_csv('data_'+user_name+'.csv')
        for i in range(len(df)):
            data_list.append((df['day'][i],df['weight_after'][i],df['weight_before'][i],df['contents'][i],df['time'][i],df['moisture'][i],df['tenki'][i],df['shitsudo'][i]))
    else:
        raise ValueError("error!")
    
    return data_list

#--Written By Mutsuyo-----------------------------------
def dassui_ritu(wb,wa):#脱水率
    z=round((wa-wb)/wb*100,1)#wb運動前　wa運動後
    return z

def hakkann_ritu(wb,wa,water,time):#1時間あたり発汗量
    z=round((wb-wa+water)/time,2)#water運動中飲水量ℓ　#time運動時間
    return z

def hakkann_ryo(wb,wa,water):#運動中発汗量(飲水必要量)
    z=round(wb-wa+water,2)
    return z

def hakkann_ritu_ex1(wb,water,time):#1時間あたり-1%発汗量
    z=round((wb-wb*0.99+water)/time,2)#water運動中飲水量ℓ　#time運動時間
    return z

def hakkann_ryo_ex1(wb,water):#運動時間あたり-1%発汗量(飲水必要量)
    z=round(wb-wb*0.99+water,2)#water運動中飲水量ℓ　#time運動時間
    return z

#--Written By Mutsuyo-----------------------------------
