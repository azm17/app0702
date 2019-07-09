# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:56:33 2019

@author: Azumi Mamiya 
         Daiki Miyagawa

pip3 install flask
pip3 install mysql-connector-python
pip3 import datetime
"""
from flask import Flask,request,render_template,make_response
import my_function2_demo as my_func
import datetime

app = Flask(__name__)
#server host
server_host='192.168.2.102'
#server_host='192.168.56.1'
#server_host='192.168.0.6'
#server_host='test-server0701.herokuapp.com'
server_port=50000
server_address=server_host+':'+str(server_port)
#server_address=server_host

#SQL server
SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'

#サーバ管理者リスト
administrators=['azumi','daiki']
user_prof={}
# 一般ユーザーログイン画面送信
@app.route("/")
def entry():
    resp = make_response(render_template('index.html',
                                         serverhost=server_address))
    resp.set_cookie('user', '')
    resp.set_cookie('pass', '')
    return resp

# 
@app.route("/hello", methods=["GET","POST"])
def hello():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} LOGIN ".format(userid),end='')
    #connect test
    try:#success
        hantei=my_func.kakunin(userid,userpass,
                               SQLserver_port,
                               SQLserver_host,
                               database_name)
    except:#fail
        hantei=False
    print(hantei)
    if hantei:# lonin success
        return render_template('hello.html', 
                               title='flask test', 
                               name=userid,
                               serverhost=server_address)
    else:# login fail
        return 'either id or pass is not match'

# 一般ユーザーの結果（表）画面
@app.route("/show", methods=["POST"])
def show():
    global user_prof
    #if request.cookies.get('user') == '':#cookieが空のときformから読み取り
    userid = request.form['user']
    userpass = request.form['pass']
    user_prof=my_func.sql_ALLuser_profile(userid,#管理者名
                                          userpass,#管理者のパスワード
                                          SQLserver_port,
                                          SQLserver_host,
                                          database_name)
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid,
                                  userid,
                                  userpass,
                                  SQLserver_port,
                                  SQLserver_host,
                                  database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
                  'date' : d['day'],#日
                  'bweight' : d['wb'],#運動前体重
                  'aweight' : d['wa'],#運動後体重
                  'training' : d['contents'],#トレーニング内容
                  'period' : d['time'],#運動時間
                  'intake' : d['moi'],#飲水量
                  'dehydraterate' : my_func.dassui_ritu(d['wb'],d['wa']),#脱水率
                  'dehydrateval' : str(float(d['wb'])-float(d['wa'])),#脱水量
                  'tenki':d['tenki'],#天気
                  'shitsudo':d['shitsudo']#湿度
                })
        latest=posts.pop(0)
        comment='いい感じです．この調子頑張りましょう!'
        messages=my_func.sql_message_get(
                userid,
                userpass,
                SQLserver_port,
                SQLserver_host,
                database_name,
                max_messages = 5
              )
        
        texts=[]
        for d in messages:
            texts.append({
                'day': d['day'],
                'rname': user_prof[d['userid']]['rname'],
                'group': d['group'],
                'title': d['title'],
                'contents': d['contents']}
            )
        print('Success')
        resp = make_response(render_template('main.html',
                                             title='My Title',
                                             user=userid,
                                             posts=posts,
                                             latest=latest,
                                             comment=comment,
                                             texts=texts,
                                             rname=user_prof[userid]['rname'],
                                             serverhost=server_address))
        resp.set_cookie('user', userid)
        resp.set_cookie('pass', userpass)
        return resp
    except Exception as error:
        return 'NG'+error.__str__()
    '''
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid,
                                  userid,
                                  userpass,
                                  SQLserver_port,
                                  SQLserver_host,
                                  database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
              'date' : str(d[0]),
              'bweight' : str(d[1]),
              'aweight' : str(d[2]),
              'training' : str(d[3]),
              'period' : str(d[4]),
              'intake' : str(d[5]),
              'dehydraterate' : str(d[6]),
              'dehydrateval' : str(d[1] - d[2])
            })
        print('Success')
        return render_template('main.html', 
                                title='My Title', 
                                user=userid, 
                                posts=posts,
                                serverhost=server_address)
    except:
        print('Fail2')
        return 'NG'
    '''
# 情報入力
@app.route("/enter", methods=["GET","POST"])
def enter():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid))
    try:
        weight_after= float(request.form['wa'])
        weight_before= float(request.form['wb'])
        contents= str(request.form['text'])
        time= float(request.form['time'])
        moisture= float(request.form['moi'])
        tenki= int(request.form['tenki'])
        shitsudo= float(request.form['sitsu'])
        my_func.sql_data_send(userid,#ログインするユーザ
                              userpass,#ログインするユーザのパス
                              SQLserver_port,
                              SQLserver_host,
                              database_name,
                              weight_after,
                              weight_before,
                              contents,time,
                              moisture,tenki,
                              shitsudo)
        
        data=my_func.sql_data_get(userid,
                                  userid,
                                  userpass,
                                  SQLserver_port,
                                  SQLserver_host,
                                  database_name)
        
        posts=[]
        for d in reversed(data):
            posts.append({
                  'date' : d['day'],#日
                  'bweight' : d['wb'],#運動前体重
                  'aweight' : d['wa'],#運動後体重
                  'training' : d['contents'],#トレーニング内容
                  'period' : d['time'],#運動時間
                  'intake' : d['moi'],#飲水量
                  'dehydraterate' : my_func.dassui_ritu(d['wb'],d['wa']),#脱水率
                  'dehydrateval' : str(float(d['wb'])-float(d['wa'])),#脱水量
                  'tenki':d['tenki'],#天気
                  'shitsudo':d['shitsudo']#湿度
                })
        latest=posts.pop(0)
        comment='いい感じです．この調子頑張りましょう!'
        messages=my_func.sql_message_get(
                userid,
                userpass,
                SQLserver_port,
                SQLserver_host,
                database_name,
                max_messages = 5
              )
        texts=[]
        for d in messages:
            texts.append({
                'day': d['day'],
                'rname': user_prof[d['userid']]['rname'],
                'group': d['group'],
                'title': d['title'],
                'contents': d['contents']}
            )
        return render_template('main.html', 
                               title='My Title',
                               user=userid,
                               posts=posts,
                               latest=latest,
                               comment=comment,
                               texts=texts,
                               rname=user_prof[userid]['rname'],
                               serverhost=server_address)
    except Exception as error:
        return error.__str__()

# for administration
#全てのユーザのプロフィールを取得：本名，組織，年度
user_prof={}
# 管理者ログインページ
@app.route("/admin")
@app.route("/admin/")
def admin_entry():
    resp = make_response(render_template('admin_index.html',
                                         serverhost=server_address))
    resp.set_cookie('user', '')
    resp.set_cookie('pass', '')
    return resp

# 管理者ホームページ
@app.route("/admin/show",methods=["POST"])
def admin_show():
    global user_prof
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    if admin == '' or adminpass == '':
        admin = request.form['user']
        adminpass = request.form['pass']
    #user情報，初めの読み込み
    user_prof=my_func.sql_ALLuser_profile(admin,#管理者名
                                          adminpass,#管理者のパスワード
                                          SQLserver_port,
                                          SQLserver_host,
                                          database_name)
    
    posts=[]
    print("ID:{} GET ".format(admin),end='')
    if admin == '' or adminpass == '':
        return 'NG: None'
    if admin in administrators: 
        try:
            hantei=my_func.kakunin(admin,
                                   adminpass,
                                   SQLserver_port,
                                   SQLserver_host,
                                   database_name)
            
            resp = make_response(render_template('admin_main.html',
                                                 title='Admin',
                                                 user=admin,
                                                 posts=posts,
                                                 serverhost=server_address))
            resp.set_cookie('user', admin)
            resp.set_cookie('pass', adminpass)
            
            if hantei:
                return resp
            return 'either id or pass is not match as administrator'
        except Exception as error:
            print('Fail')
            return 'do not connect sql server by your username \
                    \n or making html error:\n{}'.format(error.__str__())
    else:
        return 'you are not an administrator'
    ''' 
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid),end='')
    if userid in administrators:
        try:
            hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
            #resp = make_response(render_template('main.html', 
                                  title='My Title', 
                                  user=userid, 
                                  posts=posts,
                                  serverhost=server_address))
            #resp.set_cookie('user', userid)
            #resp.set_cookie('pass', userpass)
            #return resp
            if hantei:
                return 'Successful!!!!'
            return 'either id or pass is not match as administrator'
        except Exception as error:
            print('Fail')
            return 'do not connect sql server by your username\ 
                    \n or making html error:\n{}'.format(error.__str__())
    else:
        return 'you are not an administrator'
    '''
# 管理者用アプリWatch
@app.route("/admin/watch", methods=["POST"])
def admin_watch():# ユーザリスト　ユーザを選び->admin_watch_show()
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    if admin == '' or adminpass == '':
        # 不正アクセス（クッキーが空など，ユーザ名，パスワード未設定）
        return 'NG: cannot access /watch'
    
    try:
        my_func.kakunin(admin,
                        adminpass,
                        server_port,
                        server_host,
                        database_name)
    except Exception as error:
        #接続失敗，SQLに接続できないなど
        return error.__str__()
    
    posts= [{'name':user_prof[name]['rname'],
             'org':user_prof[name]['org'],
             'year':user_prof[name]['year'],
             'id':name,
             'keyword':str(user_prof[name]['year'])+user_prof[name]['org']+name,
             } for name in user_prof.keys()
    ]
    posts = reversed(sorted(posts, key=lambda x:x['keyword']))
    resp = make_response(render_template(
            'admin_watch.html',
            serverhost=server_address,
            posts=posts)
            )
    
    return resp

# 管理者用アプリwatchの内部機能 各ユーザの結果を見る
@app.route("/admin/watch/show", methods=["GET","POST"])
def admin_watch_show():
    admin = request.cookies.get('user')# クッキーを保存
    adminpass = request.cookies.get('pass')# クッキーを保存
    if admin != '' and adminpass != '':
        #SQLサーバ接続テスト：ユーザ名，パスワードの整合性の確認
        my_func.kakunin(admin,
                        adminpass,
                        server_port,
                        server_host,
                        database_name)
        uid_get=request.args.get('name')#　見たいユーザ名
        real_name=user_prof[uid_get]['rname']# 見たいユーザの本名
        
        try:
            data=my_func.sql_data_get(uid_get,# 見たいユーザ名
                                      admin,# 管理者名
                                      adminpass,#　管理者のパスワード
                                      SQLserver_port,
                                      SQLserver_host,
                                      database_name)
            posts=[]
            for d in reversed(data):#dataは辞書形式
                posts.append({
                  'date' : d['day'],#日
                  'bweight' : d['wb'],#運動前体重
                  'aweight' : d['wa'],#運動後体重
                  'training' : d['contents'],#トレーニング内容
                  'period' : d['time'],#運動時間
                  'intake' : d['moi'],#飲水量
                  'dehydraterate' : my_func.dassui_ritu(d['wb'],d['wa']),#脱水率
                  'dehydrateval' : str(float(d['wb'])-float(d['wa'])),#脱水量
                  'tenki':d['tenki'],#天気
                  'shitsudo':d['shitsudo']#湿度
                })
            print('Success')
            
            resp = make_response(
                    render_template(
                            'admin_show.html',
                            title='My Title', 
                            user=real_name,
                            posts=posts,
                            serverhost=server_address
                            )
                    )
            
            resp.set_cookie('user', admin)# クッキーの再設定
            resp.set_cookie('pass', adminpass)# クッキーの再設定
            
            return resp
        except Exception as error:# SQLなどのエラー
            return error.__str__()
    else:
        # 不正アクセス（クッキーが空など，ユーザ名，パスワード未設定）
        return 'NG: cannot access watch/show'

# 管理者用アプリNew!
@app.route("/admin/latest", methods=["POST"])
def admin_latest():
    ad_userid = request.cookies.get('user')
    ad_userpass = request.cookies.get('pass')
    if ad_userid=='' or ad_userpass=='':
        return 'cannot access!'
    try:
        print('Success')
        try:
            data=my_func.sql_data_get_latest_all(ad_userid,
                                                 ad_userpass,
                                                 SQLserver_port,
                                                 SQLserver_host,
                                                 database_name)
            
            posts=[]
            for d in reversed(data):
                posts.append({
                  'date' : d['day'],#日
                  'bweight' : d['wb'],#運動前体重
                  'aweight' : d['wa'],#運動後体重
                  'training' : d['contents'],#トレーニング内容
                  'period' : d['time'],#運動時間
                  'intake' : d['moi'],#飲水量
                  'dehydraterate' : my_func.dassui_ritu(d['wb'],d['wa']),#脱水率
                  'dehydrateval' : str(float(d['wb'])-float(d['wa'])),#脱水量
                  'tenki':d['tenki'],#天気
                  'shitsudo':d['shitsudo'],#湿度
                  'username':user_prof[d['username']]['rname']}# ユーザの本名
                )
            print('Success')
            posts = reversed(sorted(posts, key=lambda x:x['date']))
            return render_template(
                    'admin_latest.html', 
                    title='Latest posts', 
                    posts=posts,
                    serverhost=server_address
                    )
        except Exception as error:
            return error.__str__()
    except Exception as error:
            return error.__str__()

# 管理者用アプリRegister，新規ユーザー追加
@app.route("/admin/register", methods=["GET","POST"])
def admin_register():
    global user_prof
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    if len(userid)==0 or len(userpass)==0:
        return 'NG1: cannot access'
    
    if request.args.get('status')=='first':
        try:    
            my_func.kakunin(
                    userid,
                    userpass,
                    server_port,
                    server_host,
                    database_name
            )
        except Exception as error:
            return 'NG: '+error.__str__()
        posts=[]
        resp = make_response(
                render_template(
                        'admin_register.html',
                        text='',
                        serverhost=server_address,
                        posts=posts,
                        year=datetime.datetime.now().year)
                )
        
        return resp
    
    info={'newuser':request.form['newuser'],
          'newpass':request.form['newpass'],
          'rname':request.form['rname'],
          'org':request.form['org'],
          'year':request.form['year']
          }
    if len(request.form['newuser'])==0 or len(request.form['newpass'])==0 or \
        len(request.form['rname'])==0 or len(request.form['org'])==0:
        return 'NG : Fill in the blank!'
    try:
        hantei=my_func.adduser(userid,
                               userpass,
                               SQLserver_port,
                               SQLserver_host,
                               database_name,info)
        if hantei:
            resp='OK'
            resp = make_response(render_template(
                    'admin_register.html',
                    text=request.form['rname']+'さんを登録しました．',
                    serverhost=server_address,
                    year=datetime.datetime.now().year)
            )
            #user_proの更新
            user_prof=my_func.sql_ALLuser_profile(
                    userid,#管理者名
                    userpass,#管理者のパスワード
                    SQLserver_port,
                    SQLserver_host,
                    database_name
                    )
            return resp
        else:
            return 'NG'
    except Exception as error:
        return 'Fail:SQLserver Error'+error.__str__()

# 管理者用アプリ Message, 管理者から全体への連絡事項を追加
@app.route("/admin/message", methods=["GET","POST"])
def admin_message():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    messages = my_func.sql_message_get(
        userid,
        userpass,
        SQLserver_port,
        SQLserver_host, 
        database_name,
        max_messages = 10
    )
    
    posts = []
    for d in messages:
        posts.append({
            'day': d['day'],
            'rname': user_prof[d['userid']]['rname'],
            'group': d['group'],
            'title': d['title'],
            'contents': d['contents']}
        )
    
    if request.args.get('status')=='first':
        try:
            my_func.kakunin(userid,userpass,server_port,server_host,database_name)
        except Exception as error:
            return 'NG: '+error.__str__()
        resp = make_response(
                render_template(
                        'admin_message.html',
                        serverhost=server_address,
                        posts=posts)
                )
        
        return resp
    
    try:
        if len(userid)==0 or len(userpass)==0:
            return 'cannot access message'
        
        # you have to add form of group below
        group = None
        title = str(request.form['title'])
        contents = str(request.form['contents'])
        
        my_func.sql_message_send(
            userid, 
            userpass, 
            SQLserver_port, 
            SQLserver_host, 
            database_name,
            group,
            title, 
            contents,
        )
        
        messages = my_func.sql_message_get(
                userid,
                userpass,
                SQLserver_port, 
                SQLserver_host, 
                database_name,
                max_messages = 10
                )
        
        posts = []
        for d in messages:
            posts.append({
                'day': d['day'],
                'rname': user_prof[d['userid']]['rname'],
                'group': d['group'],
                'title': d['title'],
                'contents': d['contents']}
            )
        
        return render_template(
                'admin_message.html', 
                 title='Message',
                 user=userid,
                 posts=posts,
                 serverhost=server_address
                 )
    except Exception as error:
        return error.__str__()

# 管理者用アプリAnalysis，簡単な統計，解析
@app.route("/admin/analysis", methods=["GET","POST"])
def admin_analysis():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    if len(userid)==0 or len(userpass)==0:
        return 'cannot access analysis'
    return 'Analysis機能は工事中です。もうしばらくお待ちください。'

@app.route("/admin/help", methods=["GET"])
def admin_help():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    if len(userid)==0 or len(userpass)==0:
        return 'cannot access help'
    return 'Help機能は工事中です。もうしばらくお待ちください。困りごとは，間宮または宮川まで。'

if __name__ == "__main__":
    app.run(debug=False, host=server_host, port=server_port, threaded=True)
