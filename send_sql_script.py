# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 17:07:50 2020

@author: Azumi Mamiya
"""

import mysql.connector
import datetime
import csv
import time

#SQLserver_host = '192.168.0.32'
SQLserver_host = 'eiyo-kanri.taberube.jp'
# SQLserver_host = 
SQLserver_port = 3306
database_name = 'dehydration2'
# sql_userid = 'mutsu624'
sql_userpass = '624mutsu'

user_name = ''
user_pass = ''

def get_user_dic():
    user_dic = {}
    conn = mysql.connector.connect(
        host = SQLserver_host,
        port = SQLserver_port,
        user = sql_userid,
        password = sql_userpass,
        database = database_name,
    )
    cur = conn.cursor()
    connected = conn.is_connected()
    if (not connected):
        conn.ping(True)
    cur.execute('''SELECT `{}`,`{}` FROM `{}` '''
                .format("id", "password", "user_list"))
    for row in cur.fetchall():
        user_dic[row[0]] = row[1]
    return user_dic

def sql_data_send(user_name,
                  user_pass,
                  bweight,
                  aweight,
                  training,
                  time,
                  water,
                  weather,
                  humidity,
                  temp,
                  date):
    
    user_dic = get_user_dic()
    if user_pass == user_dic[user_name]:
        user_dic = get_user_dic()
        
        conn = mysql.connector.connect(
            host = SQLserver_host,
            port = SQLserver_port,
            user = sql_userid,
            password = sql_userpass,
            database = database_name,
        )
        cur = conn.cursor()
        connected = conn.is_connected()
        
        if (not connected):
            conn.ping(True)
        Rtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")\
                 + user_name
        # tmp_day = datetime.date.today()
        day = date
        cur.execute(
                '''INSERT INTO `{}` (`id`,`day`, `weather`, `humidity`, 
                `training`,`time`, `bweight`,`aweight`,`water`,`temp`,`rtime`) 
                    VALUES ('{}', '{}', {}, {},'{}',{},{},{},{},{},'{}')
                '''.format('data', user_name, day, weather, humidity,
                            training, time, bweight, aweight, water,
                            temp, Rtime)
                    )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return  'OK'
    return  'NG'

def send(row):
    date    = row[0]
    weather = row[1]
    temp    = row[2]
    humidity = row[3]
    training = row[4]
    bweight =row[5]
    aweight  = row[6]
    water = row[7]
    time = row[8]
    
    
    sql_data_send(user_name, 
                  user_pass, 
                  bweight,
                  aweight,
                  training,
                  time,
                  water,
                  weather,
                  humidity,
                  temp,
                  date)

def read_csv():
    with open('data2.csv', encoding="utf-8") as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            print(row)
            send(row)
            time.sleep(2)

read_csv()