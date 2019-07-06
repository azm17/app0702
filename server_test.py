# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:56:33 2019

@author: Azumi Mamiya

pip3 install flask
pip3 install mysql-connector-python
"""
from flask import Flask,request,render_template
from flask import Flask, make_response
import my_function2_demo as my_func
import sys

app = Flask(__name__)
#server host
#server_host='test-server0701.herokuapp.com'
server_host='192.168.2.102'
server_port=50000
server_address=server_host+':'+str(server_port)
#SQL server
SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'

administrators=['azumi','daiki']

@app.route("/")
def entry():
    resp = make_response(render_template('index.html',serverhost=server_address))
    resp.set_cookie('user', '')
    resp.set_cookie('pass', '')
    return resp

@app.route("/hello", methods=["GET","POST"])
def hello():
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} LOGIN ".format(userid),end='')
    #connect test
    try:#success
        hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
    except:#fail
        hantei=False
    print(hantei)
    if hantei:
        return render_template('hello.html', title='flask test', name=userid,serverhost=server_address)# lonin success
    else:
        return 'either id or pass is not match'# login fail

@app.route("/show", methods=["POST"])
def show():
    if request.cookies.get('user') == '':
        userid = request.form['user']
        userpass = request.form['pass']
        print("ID:{} GET ".format(userid),end='')
        try:
            data=my_func.sql_data_get(userid,userid,userpass,SQLserver_port,SQLserver_host,database_name)
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
            resp = make_response(render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_address))
            resp.set_cookie('user', userid)
            resp.set_cookie('pass', userpass)
            return resp
        except:
            print('Fail1')
            return 'NG'
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid,userid,userpass,SQLserver_port,SQLserver_host,database_name)
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
        return render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_address)
    except:
        print('Fail2')
        return 'NG'

@app.route("/enter", methods=["GET","POST"])
def enter():
    #userid = request.form['user']
    #userpass = request.form['pass']
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
        my_func.sql_data_send(userid,userpass,SQLserver_port,SQLserver_host,database_name,weight_after,weight_before,contents,time,moisture,tenki,shitsudo)
        data=my_func.sql_data_get(userid,userid,userpass,SQLserver_port,SQLserver_host,database_name)
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

        return render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_address)
        #return render_template('result.html', title='My Title', user=userid, posts=posts)
    except Exception as error:
        return error.__str__()

# administration page
# 管理者ログインページ
@app.route("/admin")
@app.route("/admin/")
def admin_entry():
    resp = make_response(render_template('admin_index.html',serverhost=server_address))
    resp.set_cookie('user', '')
    resp.set_cookie('pass', '')
    return resp

# 管理者ホームページ
@app.route("/admin/show",methods=["POST"])
def admin_show():
    if request.cookies.get('user') == '':
        userid = request.form['user']
        userpass = request.form['pass']
        posts=[]
        print("ID:{} GET ".format(userid),end='')
        if userid in administrators:
            try:
                hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
                resp = make_response(render_template('admin_main.html', title='Admin', user=userid, posts=posts,serverhost=server_address))
                #resp.set_cookie('user', userid)
                #resp.set_cookie('pass', userpass)
                
                if hantei:
                    return resp
                return 'either id or pass is not match as administrator'
            except Exception as error:
                print('Fail')
                return 'do not connect sql server by your username \n or making html error:\n{}'.format(error.__str__())
        else:
            return 'you are not an administrator'
    ''' 
    userid = request.cookies.get('user')
    userpass = request.cookies.get('pass')
    print("ID:{} GET ".format(userid),end='')
    if userid in administrators:
        try:
            hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
            #resp = make_response(render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_address))
            #resp.set_cookie('user', userid)
            #resp.set_cookie('pass', userpass)
            #return resp
            if hantei:
                return 'Successful!!!!'
            return 'either id or pass is not match as administrator'
        except Exception as error:
            print('Fail')
            return 'do not connect sql server by your username \n or making html error:\n{}'.format(error.__str__())
    else:
        return 'you are not an administrator'
    '''
# 管理者用アプリWatch
@app.route("/admin/watch", methods=["GET","POST"])
def admin_watch():
    #userid = request.form['user']
    #userpass = request.form['pass']
    userid='azumi'
    userpass='mamiya'
    
    user_prof=my_func.sql_ALLuser_profile(userid,userpass,SQLserver_port,SQLserver_host,database_name)
    posts= [{'name':user_prof[name]['rname'], \
             'id':name \
             } for name in user_prof.keys()\
    ]
    resp = make_response(render_template('admin_watch.html',serverhost=server_address,posts=posts))
    return resp

# 管理者用アプリwatchの内部機能
@app.route("/admin/watch/show", methods=["GET","POST"])
def admin_watch_show():
    #userid = request.form['user']
    #userpass = request.form['pass']
    
    admin='azumi'
    adminpass='mamiya'
    user_prof=my_func.sql_ALLuser_profile(admin,adminpass,SQLserver_port,SQLserver_host,database_name)
    uid_get=request.args.get('name')
    real_name=user_prof[uid_get]['rname']
    try:
        data=my_func.sql_data_get(uid_get,admin,adminpass,SQLserver_port,SQLserver_host,database_name)
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
        
        resp = make_response(render_template('admin_show.html', title='My Title', user=real_name, posts=posts,serverhost=server_address))
        resp.set_cookie('user', admin)
        resp.set_cookie('pass', adminpass)
        return resp
    except Exception as error:
        return error.__str__()

# 管理者用アプリNew!
@app.route("/admin/latest")
def admin_latest():
    ad_userid = request.cookies.get('user')
    ad_userpass = request.cookies.get('pass')
    #if userid in administrator:
    if True:
        print('Success')
        try:
            data=my_func.sql_data_get_latest_all(ad_userid, ad_userpass,SQLserver_port,SQLserver_host,database_name)
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
                  'dehydrateval' : str(d[1] - d[2]),
                  'username': str(d[8]),
                })
            print('Success')
            return render_template('admin_latest.html', title='Latest posts', posts=posts,serverhost=server_address)
        except Exception as error:
            return error.__str__()
    else:
        print('Fail')
        return 'you are not an administrator'

# 管理者用アプリRegister，新規ユーザー追加
@app.route("/admin/register", methods=["GET","POST"])
def admin_register():
    #userid = request.form['user']
    #userpass = request.form['pass']
    
    #userid='azumi'
    #userpass='mamiya'
    #namelist=my_func.sql_username_list(userid,userpass,SQLserver_port,SQLserver_host,database_name)
    userid='azumi'
    userpass='mamiya'
    if request.args.get('status')=='first':
        posts=[]
        resp = make_response(render_template('admin_register.html',serverhost=server_address,posts=posts))
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
        hantei=my_func.adduser(userid,userpass,SQLserver_port,SQLserver_host,database_name,info)
        if hantei:
            resp='OK'
            resp = make_response(render_template('admin_register.html',serverhost=server_address))
            return resp
        else:
            return 'NG'
    except Exception as error:
        return 'Fail:SQLserver Error'+error.__str__()
    
# 管理者用アプリRegister内部機能，新規ユーザー情報送信
@app.route("/admin/register_submit", methods=["GET","POST"])
def admin_register_submit():
    #userid = request.form['user']
    #userpass = request.form['pass']
    userid='azumi'
    userpass='mamiya'
    info={'newuser':request.form['newuser'],
          'newpass':request.form['newpass'],
          'rname':request.form['rname'],
          'org':request.form['org'],
          'year':request.form['year']
          }
    try:
        hantei=my_func.adduser(userid,userpass,SQLserver_port,SQLserver_host,database_name,info)
        if hantei:
            resp='OK'
            resp = make_response(render_template('admin_register.html',serverhost=server_address))
            return resp
        else:
            return 'NG'
    except Exception as error:
        return 'Fail:SQLserver Error'+error.__str__()

# 管理者用アプリAnalysis，簡単な統計，解析
@app.route("/admin/analysis", methods=["GET","POST"])
def admin_analysis():
    return '工事中'



if __name__ == "__main__":
    app.run(debug=False, host=server_host, port=server_port, threaded=True)
