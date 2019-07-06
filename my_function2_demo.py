# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:30 2019

@author: azumi
"""

#import mysql.connector
import datetime
import pandas as pd

def get_user_dic(user_name,user_pass,port,host,db_name):
    user_dic={}
    df = pd.read_csv('user_list.csv', index_col=0)
    for i in range(len(df)):
        user_dic[df.at[i,'username']]=df.at[i,'pass']
    return user_dic

def sql_ALLuser_profile(user_name,user_pass,port,host,db_name):
    user_prof={}
    df = pd.read_csv('user_list.csv', index_col=0)
    for i in range(len(df)):
        user_prof[df.at[i,'username']]={'rname':df.at[i,'rname'],'org':df.at[i,'org'],'year':df.at[i,'year']}
    return user_prof

def sql_username_list(user_name,user_pass,port,host,db_name):
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        return list(user_dic.keys())
    return 'NG'

def kakunin(user_name,user_pass,port,host,db_name):
    connected=False
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        connected=True
    return connected

def sql_data_send(user_name,user_pass,port,host,db_name,weight_after,weight_before,contents,time,moisture,tenki,shitsudo):
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        df = pd.read_csv('data_'+user_name+'.csv', index_col=0)
        tmp_day=datetime.date.today()
        day=tmp_day.strftime('%Y-%m-%d')
        #df.append(day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo)
        columns = ["day","weight_after","weight_before","contents","time","moisture","tenki","shitsudo"]
        tmp_se = pd.Series([day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo], index=columns, name=str(df.shape[0]))
        df = df.append(tmp_se)
        #print(df.head())
        df.to_csv('data_'+user_name+'.csv',encoding="utf-8")
    return  'OK'

def sql_data_get(user_nm,user_name,user_pass,port,host,db_name):
    #user_name ←のアカウントを使って
    #user_nm ←のデータを取得
    data_list=[]
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    if user_pass==user_dic[user_name]:
        df = pd.read_csv('data_'+user_nm+'.csv')
        for i in range(len(df)):
            data_list.append((df['day'][i],df['weight_after'][i],df['weight_before'][i],df['contents'][i],df['time'][i],df['moisture'][i],df['tenki'][i],df['shitsudo'][i]))
    else:
        raise ValueError("error!")
    
    return data_list

def sql_data_get_latest_all(user_name, user_pass, port, host, db_name):
    now = datetime.date.today()#.strftime('%Y-%m-%d')
    data_list=[]
    user_dic=get_user_dic(user_name,user_pass,port,host,db_name)
    for u_name in user_dic.keys():
        df = pd.read_csv('data_'+u_name+'.csv')
        for i in range(len(df)):
            tstr = df['day'][i] # string of date
            tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d')
            tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
            delta = now - tdate
            if delta.days < 2:
                data_list.append((df['day'][i],df['weight_after'][i],df['weight_before'][i],df['contents'][i],df['time'][i],df['moisture'][i],df['tenki'][i],df['shitsudo'][i],u_name))
    
    return data_list


def adduser(userid,userpass,SQLserver_port,SQLserver_host,database_name,info):
    df = pd.read_csv('user_list.csv', index_col=0)
    columns = ["username","pass","rname","org","year"]
    tmp_se = pd.Series([info['newuser'],info['newpass'],info['rname'],info['org'],info['year']], index=columns, name=str(df.shape[0]))
    df = df.append(tmp_se)
    df.to_csv('user_list.csv',encoding="utf-8")
    
    columns = ["day","weight_after","weight_before","contents","time","moisture","tenki","shitsudo"]
    f = open('data_'+info['newuser']+'.csv','w')
    f.write(',day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo\n')
    f.close()
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
