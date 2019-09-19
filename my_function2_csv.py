# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:30 2019

@author: Azumi Mamiya
         Daiki Miyagawa
"""

#import mysql.connector
import datetime
import pandas as pd

SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'
sql_userid='sql_azumi'
sql_userpass='sql_mamiya'

#すべてのユーザーのIDとパスを表示
def get_user_dic():
    user_dic={}
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis")#ユーザーリストからidとpassを取得
    for i in range(len(df)):
        user_dic[df.at[i,'id']]=df.at[i,'password']
    return user_dic

def get_user_info():
    user_info=[]
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis")#ユーザーリストからidとpassを取得
    for i in range(len(df)):
        user_info.append({'id':df.at[i,'id'],
                          'password':df.at[i,'password'],
                          'type':str(df.at[i,'type']),
                          'rname':df.at[i,'rname'],
                          'org':df.at[i,'org'],
                          'year':df.at[i,'org']})
    return user_info

def sql_ALLuser_profile(user_name, user_pass):
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

#ログイン処理
def kakunin(user_name, user_pass):
    connected=False
    user_dic=get_user_dic()
    if user_name in user_dic.keys():
        if user_pass==user_dic[user_name]:
            connected=True
    return connected

def admin_kakunin(user_name, user_pass):
    connected=False
    user_info=get_user_info()
    for i in range(len(user_info)):
        if user_name==user_info[i]['id'] \
            and user_pass==user_info[i]['password'] \
                and user_info[i]['type']=='0':
            connected=True
            break
    return connected
def get_admin():
    user_info=get_user_info()
    admin=[]
    for i in range(len(user_info)):
        if user_info[i]['type']=='0':
            admin.append(user_info[i]['id'])
    return admin
#print(admin_kakunin('azumi','mamiya'))

def sql_data_send(user_name,
                  user_pass,
                  bweight,
                  aweight,
                  training,
                  time,
                  water,
                  weather,
                  humidity,
                  temp):
    
    user_dic=get_user_dic()
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
                   "water",
                   "temp",
                   "rtime"]
        Rtime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        tmp_se = pd.Series([user_name,
                            day,
                            weather,
                            humidity,
                            training,
                            time,
                            bweight,
                            aweight,
                            water,
                            temp,
                            Rtime], index=columns, name=str(df.shape[0]))
        df = df.append(tmp_se)
        df.to_csv('./database/data.csv',encoding="shift-jis")
    return  'OK'
 
def sql_data_get(user_nm):
    #user_name ←のアカウントを使って
    #user_nm ←のデータを取得
    data_list=[]
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
                          'shitsudo':df['humidity'][i],
                          'temp':df['temp'][i]})#湿度
    data_list.sort(key=lambda x:x['day'])
    
    return data_list

def sql_data_get_latest_all():
    now = datetime.date.today()#.strftime('%Y-%m-%d')
    data_list=[]
    user_dic=get_user_dic()
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
                              'username':u_name,
                              'temp':df['temp'][i]})#湿度
                
                data_list.sort(key=lambda x:x['day'])
                data_list.reverse()
    
    return data_list

def sql_message_send(userid,
                     userpass,
                     group,
                     title,
                     contents):

    user_dic=get_user_dic()
    
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


def sql_message_get(userid, userpass, max_messages = 10):
    
    user_dic=get_user_dic()
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

def adduser(admin,adminpass,info):
    df = pd.read_csv('./database/user_list.csv',
                     index_col=0,
                     encoding="shift-jis"
                     )
    columns = ["id","password","type","rname","org","year"]
    tmp_se = pd.Series([info['newuser'],
                        info['newpass'],
                        info['type'],
                        info['rname'],
                        info['org'],
                        info['year']],
                        index=columns,
                        name=str(df.shape[0]))
    
    df = df.append(tmp_se)
    df.to_csv('./database/user_list.csv',encoding="shift-jis")
    
    return 'OK'

def sql_data_per_day(day):
    #user_name ←のアカウントを使って
    #user_nm ←のデータを取得
    data_list=[]
    tmp_df = pd.read_csv('./database/data.csv',
                     index_col=0,
                     encoding="shift-jis")
    
    df=tmp_df[tmp_df['day'] ==day].reset_index()
    data_list=[]
    for i in range(len(df)):
        data_list.append({'day':df['day'][i],#日
                          'wa':df['aweight'][i],#運動後体重
                          'wb':df['bweight'][i],#運動前体重
                          'contents':df['training'][i],#トレーニング内容
                          'time':df['time'][i],#時間
                          'moi':df['water'][i],#飲水量
                          'tenki':df['weather'][i],#天気
                          'shitsudo':df['humidity'][i],
                          'temp':df['temp'][i]})#湿度
    
    return data_list

def sql_makecsv(file):
    return True
#--Written By Mutsuyo-----------------------------------
def dassui_ritu(wb,wa):#脱水率
    z=round((wa-wb)/wb*100,1)#wb運動前　wa運動後
    return z

def hakkann_ritu(wb,wa,water,time):#1時間あたり発汗量
    z=round((wb-wa+water)/time,2)#water運動中飲水量?　#time運動時間
    return z

def hakkann_ryo(wb,wa,water):#運動中発汗量(飲水必要量)
    z=round(wb-wa+water,2)
    return z

def hakkann_ritu_ex1(wb,water,time):#1時間あたり-1%発汗量
    z=round((wb-wb*0.99+water)/time,2)#water運動中飲水量?　#time運動時間
    return z

def hakkann_ryo_ex1(wb,water):#運動時間あたり-1%発汗量(飲水必要量)
    z=round(wb-wb*0.99+water,2)#water運動中飲水量?　#time運動時間
    return z

#--Written By Mutsuyo-----------------------------------

def generateComment(data):
    sentence='おつかれさま。'
    if 0<=data['dehydraterate']:
        sentence+='トレーニング中水分補給がんばった!!'
        img='suzuki1.jpg'
    elif -1.0<data['dehydraterate']<0:
        sentence+='トレーニング中の水分補給大事。この調子!!'
        img='suzuki2.jpg'
    elif -2.0<=data['dehydraterate']<=-1.0:
    #elif -1.0 < data['dehydraterate']:
        sentence+='水分補給もう少し。目指せ脱水率-1%以内でパフォーマンスup!'
        img='suzuki3.jpg'
    elif data['dehydraterate']<-2.0:
        sentence+='''トレーニング中水分不足だよ。水分補給を増やして、
                    熱中症や食欲不振を予防しよう。目指せ脱水率-1%以内。'''
        img='suzuki4.jpg'
    else:
        img='suzuki1.jpg'
        sentence='ERROR'
    return {'sentence':sentence,'img':img}