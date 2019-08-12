# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:30 2019

@author: azumi
"""

#import mysql.connector
import datetime
import pandas as pd


#すべてのユーザーのIDとパスを表示
def get_user_dic(user_name,user_pass,port,host,db_name):
    user_dic={}
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis")#ユーザーリストからidとpassを取得
    for i in range(len(df)):
        user_dic[df.at[i,'id']]=df.at[i,'password']
    
    return user_dic

def sql_ALLuser_profile(user_name,user_pass,port,host,db_name):
    user_prof={}
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis")#すべてのユーザのpass以外情報を取得
    for i in range(len(df)):
        user_prof[df.at[i,'id']]={'rname':df.at[i,'rname'],
                                  'type':df.at[i,'type'],
                                  'org':df.at[i,'org'],
                                  'year':df.at[i,'year']}
    return user_prof

def sql_username_list(user_name,user_pass,port,host,db_name):
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        return list(user_dic.keys())
    return 'NG'

#ログイン処理
def kakunin(user_name,user_pass,port,host,db_name):
    connected=False
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        connected=True
    return connected

def sql_data_send(user_name,
                  user_pass,
                  port,host,
                  db_name,
                  weight_after,
                  weight_before,
                  contents,
                  time,
                  moisture,
                  tenki,
                  shitsudo):
    
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        df = pd.read_csv('./database/data.csv',
                         index_col=0,
                         encoding="shift-jis")
        
        tmp_day=datetime.date.today()
        day=tmp_day.strftime('%Y-%m-%d')
        columns = ["id",
                   "day",
                   "weather",
                   "humidity",
                   "training",
                   "time",
                   "bweight",
                   "aweight",
                   "water"                   
                   ]
        tmp_se = pd.Series([user_name,
                            day,
                            weight_after,
                            weight_before,
                            contents,
                            time,
                            moisture,
                            tenki,
                            shitsudo], index=columns, name=str(df.shape[0]))
        df = df.append(tmp_se)
        df.to_csv('./database/data.csv',encoding="shift-jis")
    return  'OK'

def sql_data_get(user_nm,user_name,user_pass,port,host,db_name):
    #user_name ←のアカウントを使って
    #user_nm ←のデータを取得
    data_list=[]
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        tmp_df = pd.read_csv('./database/data.csv',
                         index_col=0,
                         encoding="shift-jis")
        
        df=tmp_df[tmp_df['id'] ==user_nm].reset_index()
        data_list=[]
        for i in range(len(df)):
            data_list.append({'day':df['day'][i],#日
                              'wa':df['aweight'][i],#運動後体重
                              'wb':df['bweight'][i],#運動前体重
                              'contents':df['training'][i],#トレーニング内容
                              'time':df['time'][i],#時間
                              'moi':df['water'][i],#飲水量
                              'tenki':df['weather'][i],#天気
                              'shitsudo':df['humidity'][i]})#湿度
    else:
        raise ValueError("error!")
    
    return data_list

def sql_data_get_latest_all(user_name, user_pass, port, host, db_name):
    now = datetime.date.today()#.strftime('%Y-%m-%d')
    data_list=[]
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    for u_name in user_dic.keys():
        tmp_df = pd.read_csv('./database/data.csv',
                         encoding="shift-jis")
        df=tmp_df[tmp_df['id'] ==u_name].reset_index()
        for i in range(len(df)):
            tstr = df['day'][i] # string of date
            tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
            delta = now - tdate
            if delta.days < 2:
                data_list.append({'day':df['day'][i],#日
                              'wa':df['aweight'][i],#運動後体重
                              'wb':df['bweight'][i],#運動前体重
                              'contents':df['training'][i],#トレーニング内容
                              'time':df['time'][i],#時間
                              'moi':df['water'][i],#飲水量
                              'tenki':df['weather'][i],#天気
                              'shitsudo':df['humidity'][i],
                              'username':u_name})#湿度
                data_list.sort(key=lambda x:x['day'])
                data_list.reverse()
    
    return data_list

def sql_message_send(userid,
                     userpass,
                     SQLserver_port, 
                     SQLserver_host,
                     database_name, 
                     group,
                     title,
                     contents):

    user_dic=get_user_dic(userid,
                          userpass,
                          SQLserver_port,
                          SQLserver_host,
                          database_name)
    
    if userpass==user_dic[userid]:
        df = pd.read_csv('./database/board.csv',
                         index_col=0,
                         encoding="shift-jis")
        columns = ["day",
                   "to",
                   "from",
                   "title",
                   "contents",
        ]

        tmp_day=datetime.date.today()
        day=tmp_day.strftime('%Y-%m-%d')
        tmp_se = pd.Series([day,
                            "ALL",  # you have to change!
                            userid,
                            title, 
                            contents,
                           ], index=columns, name=str(df.shape[0]))
        df = df.append(tmp_se)
        df.to_csv('./database/board.csv',encoding="shift-jis")
        return  'OK'
    return 'Not found'


def sql_message_get(userid, userpass, SQLserver_port, SQLserver_host,
                    database_name, max_messages = 10):
    
    user_dic=get_user_dic(userid,userpass,SQLserver_port,
                          SQLserver_host,database_name)
    data_list = []
    if userpass==user_dic[userid]:
        df = pd.read_csv('./database/board.csv',
                         encoding="shift-jis")
        for i in range(len(df)):
            data_list.append({
                'day':df['day'][i],#日
                'userid':df['from'][i],
                'group': df['to'][i],
                'title': df['title'][i],
                'contents': df['contents'][i],
            })
            data_list.sort(key=lambda x:x['day'])
            data_list.reverse()
    
    if len(data_list) > max_messages:
        return data_list[:max_messages]
    return data_list    

def adduser(userid,userpass,SQLserver_port,SQLserver_host,database_name,info):
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis"
                     )
    columns = ["id","password","type","rname","org","year"]
    tmp_se = pd.Series([info['newuser'],
                        info['newpass'],
                        1,
                        info['rname'],
                        info['org'],
                        info['year']],
                        index=columns,
                        name=str(df.shape[0]))
    
    df = df.append(tmp_se)
    df.to_csv('./database/user_list.csv',encoding="shift-jis")
    
    return 'OK'

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
