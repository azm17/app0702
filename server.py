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
server_host='192.168.0.15'
#server_host='192.168.2.102'
#server_host='192.168.56.1'
#server_host='192.168.0.6'
#server_host='test-server0701.herokuapp.com'


# serverport
server_port=50000
server_address=server_host+':'+str(server_port)
#server_address=server_host

#SQL server
SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'
sql_userid='sql_azumi'
sql_userpass='sql_mamiya'

tenki_dic={'1':'晴れ','2':'曇り','3':'雨','4':'雪'}
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
    hantei=my_func.kakunin(userid,userpass)
    print("ID:{} TRY LOGIN "+str(hantei).format(userid))
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
    userid = request.form['user']
    userpass = request.form['pass']
    user_prof=my_func.sql_ALLuser_profile()
    
    if my_func.kakunin(userid,userpass):
        pass
    else:
        return 'kakunin error'
    
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid)
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
                  'dehydrateval' : str(round(float(d['wb'])-float(d['wa']),1)),#脱水量
                  'tenki':str(tenki_dic[str(d['tenki'])]),#天気
                  'shitsudo':d['shitsudo'],#湿度
                  'temp':d['temp'],
                  'dassui1':round(my_func.hakkann_ritu_ex1(d['wb'],d['wa'],d['time']),1),
                  'necessary':round(my_func.hakkann_ryo(d['wb'],d['wa'],d['moi']),1),
                  'necessary1':'null',
                  'w1':round(d['wb']*0.99,1)
                })
        if len(posts)>0:
            latest=posts.pop(0)
            comment=my_func.generateComment(latest)
        else:
            latest={
                  'date' : '今回',#日
                  'bweight' : 'No data',#運動前体重
                  'aweight' : 'No data',#運動後体重
                  'training' : 'No data',#トレーニング内容
                  'period' : 'No data',#運動時間
                  'intake' : 'No data',#飲水量
                  'dehydraterate' : 'No data',#脱水率
                  'dehydrateval' : 'No data',#脱水量
                  'tenki':'No data',#天気
                  'shitsudo':'No data',#湿度
                  'temp':'No data',
                  'dassui1':'No data',
                  'necessary':'No data',
                  'necessary1':'No data',
                  'w1':'No data'}
            comment='''初めまして。このアプリでは、
                日々のトレーニング後の脱水量を記録していきます。
                最初のデータを入力しましょう。
                下の「データ入力」ボタンから結果を登録できます。'''
        messages=my_func.sql_message_get(
                userid,
                userpass,
                max_messages = 3)
        
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
        return 'NG: '+error.__str__()

# 情報入力
@app.route("/enter", methods=["GET","POST"])
def enter():
    user_prof=my_func.sql_ALLuser_profile()
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    
    if my_func.kakunin(userid,userpass):
        pass
    else:
        return 'kakunin error'
    
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
                              weight_before,
                              weight_after,
                              contents,time,
                              moisture,tenki,
                              shitsudo)
        
        data=my_func.sql_data_get(userid)
        
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
                  'dehydrateval' : str(round(float(d['wb'])-float(d['wa']),1)),#脱水量
                  'tenki':str(tenki_dic[str(d['tenki'])]),#天気
                  'shitsudo':d['shitsudo'],#湿度
                  'temp':d['temp'],
                  'dassui1':round(my_func.hakkann_ritu_ex1(d['wb'],d['wa'],d['time']),1),
                  'necessary':round(my_func.hakkann_ryo(d['wb'],d['wa'],d['moi']),1),
                  'necessary1':'null',
                  'w1':round(d['wb']*0.99,1)
                })
        
        latest=posts.pop(0)
        comment=my_func.generateComment(latest)
        messages=my_func.sql_message_get(
                userid,
                userpass,
                max_messages=3)
        
        texts=[]
        for d in messages:
            texts.append({
                'day': d['day'],
                'rname': user_prof[d['userid']]['rname'],
                'group': d['group'],
                'title': d['title'],
                'contents': d['contents']})
        
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
        return 'error: '+error.__str__()

# for administration
#全てのユーザのプロフィールを取得：本名，組織，年度
#user_prof={}
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
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
        
    if admin == '' or adminpass == '':
        admin = request.form['user']
        adminpass = request.form['pass']
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
        
    posts=[]
    print("ID:{} GET ".format(admin),end='')
    if admin == '' or adminpass == '':
        return 'NG: None'
    administrators=my_func.get_admin()
    if admin in administrators: 
        try:
            hantei=my_func.kakunin(admin,adminpass)
            
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
    
# 管理者用アプリWatch
@app.route("/admin/watch", methods=["POST"])
def admin_watch():# ユーザリスト　ユーザを選び->admin_watch_show()
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    user_prof=my_func.sql_ALLuser_profile()
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    if admin == '' or adminpass == '':
        # 不正アクセス（クッキーが空など，ユーザ名，パスワード未設定）
        return 'NG: cannot access /watch'
    
    try:
        my_func.kakunin(admin,adminpass)
    except Exception as error:
        #接続失敗，SQLに接続できないなど
        return 'ERORR: '+error.__str__()
    
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
            posts=posts))
    
    return resp

# 管理者用アプリwatchの内部機能 各ユーザの結果を見る
@app.route("/admin/watch/show", methods=["GET","POST"])
def admin_watch_show():
    admin = request.cookies.get('user')# クッキーを保存
    adminpass = request.cookies.get('pass')# クッキーを保存
    user_prof = my_func.sql_ALLuser_profile()
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    if admin != '' and adminpass != '':
        #SQLサーバ接続テスト：ユーザ名，パスワードの整合性の確認
        my_func.kakunin(admin,adminpass)
        uid_get=request.args.get('name')#　見たいユーザ名
        real_name=user_prof[uid_get]['rname']# 見たいユーザの本名
        
        try:
            data=my_func.sql_data_get(uid_get)
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
                  'dehydrateval' : str(round(float(d['wb'])-float(d['wa']),1)),#脱水量
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
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    user_prof=my_func.sql_ALLuser_profile()
    
    if admin=='' or adminpass=='':
        return 'cannot access!'
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    try:
        print('Success')
        try:
            data=my_func.sql_data_get_latest_all()
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
                  'dehydrateval' : str(round(float(d['wb'])-float(d['wa']),1)),#脱水量
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
                    serverhost=server_address)
            
        except Exception as error:
            return 'ERROR1: '+error.__str__()
    except Exception as error:
            return 'ERROR2: '+error.__str__()

# 管理者用アプリRegister，新規ユーザー追加
@app.route("/admin/register", methods=["GET","POST"])
def admin_register():
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    if len(admin)==0 or len(adminpass)==0:
        return 'NG1: cannot access'
    
    if request.args.get('status')=='first':
        try:    
            my_func.kakunin(admin, adminpass)
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
        hantei=my_func.adduser(admin,
                               adminpass,
                               info)
        if hantei:
            resp='OK'
            resp = make_response(render_template(
                    'admin_register.html',
                    text=request.form['rname']+'さんを登録しました．',
                    serverhost=server_address,
                    year=datetime.datetime.now().year)
            )
            #user_proの更新
            #user_prof=my_func.sql_ALLuser_profile()
            return resp
        else:
            return 'NG'
    except Exception as error:
        return 'Fail:SQLserver Error'+error.__str__()

# 管理者用アプリ Message, 管理者から全体への連絡事項を追加
@app.route("/admin/message", methods=["GET","POST"])
def admin_message():
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    user_prof=my_func.sql_ALLuser_profile()
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    messages = my_func.sql_message_get(
        admin,
        adminpass,
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
            my_func.kakunin(admin, adminpass)
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
        if len(admin)==0 or len(adminpass)==0:
            return 'cannot access message'
        
        # you have to add form of group below
        group = None
        title = str(request.form['title'])
        contents = str(request.form['contents'])
        
        my_func.sql_message_send(
            admin, 
            adminpass, 
            group,
            title, 
            contents,
        )
        
        messages = my_func.sql_message_get(
                admin,
                adminpass,
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
                 user=admin,
                 posts=posts,
                 serverhost=server_address
                 )
    except Exception as error:
        return error.__str__()

# 管理者用アプリAnalysis，簡単な統計，解析
@app.route("/admin/analysis", methods=["GET","POST"])
def admin_analysis():
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    if len(admin)==0 or len(adminpass)==0:
        return 'cannot access analysis'
    return 'Analysis機能は工事中です。もうしばらくお待ちください。'

@app.route("/admin/help", methods=["GET"])
def admin_help():
    admin = request.cookies.get('user')
    adminpass = request.cookies.get('pass')
    
    if my_func.admin_kakunin(admin, adminpass):
        pass
    else:
        return 'admin_kakunin error'
    
    if len(admin)==0 or len(adminpass)==0:
        return 'cannot access help'
    return 'Help機能は工事中です。もうしばらくお待ちください。困りごとは，間宮または宮川まで。'

if __name__ == "__main__":
    app.run(debug=False,
            host=server_host,
            port=server_port,
            threaded=True
            )

