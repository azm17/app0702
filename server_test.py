# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:56:33 2019

@author: Azumi Mamiya

pip3 install flask
pip3 install mysql-connector-python
"""
from flask import Flask,request,render_template
import my_function2_demo as my_func

app = Flask(__name__)
#server host
server_host='192.168.0.12'
server_port=50000
#SQL server
SQLserver_host='192.168.0.32'
SQLserver_port=3306
database_name='hydration_db'

@app.route("/")
def entry():
    html = render_template('index.html',serverhost=server_host,serverport=server_port)
    return html

@app.route("/hello", methods=["GET","POST"])
def hello():
    userid = request.form['user']
    userpass = request.form['pass']
    print("ID:{} LOGIN ".format(userid),end='')
    #connect test
    try:#success
        hantei=my_func.kakunin(userid,userpass,SQLserver_port,SQLserver_host,database_name)
    except:#fail
        hantei=False
    print(hantei)
    if hantei:
        return render_template('hello.html', title='flask test', name=userid,serverhost=server_host,serverport=server_port)# lonin success
    else:
        return 'either id or pass is not match'# login fail

@app.route("/show", methods=["POST"])
def show():
    userid = request.form['user']
    userpass = request.form['pass']
    print("ID:{} GET ".format(userid),end='')
    try:
        data=my_func.sql_data_get(userid,userpass,SQLserver_port,SQLserver_host,database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
              'date' : str(d[0]),
              'training' : str(d[3]),
              'bweight' : str(d[1]),
              'aweight' : str(d[2]),
              'dehydrateval' : str(d[4]),
              'dehydraterate' : str(d[5]),
              'intake' : str(d[6]),
              'period' : str(d[7])
            })
        print('Success')
        return render_template('main.html', title='My Title', user=userid, posts=posts,serverhost=server_host,serverport=server_port)
    except:
        print('Fail')
        return 'NG'

#@app.route("/entry", methods=["POST"])
@app.route("/enter", methods=["GET","POST"])
def enter():
    userid = request.form['user']
    userpass = request.form['pass']
    try:
        weight_after= float(request.form['wa'])
        weight_before= float(request.form['wb'])
        contents= str(request.form['text'])
        time= float(request.form['time'])
        moisture= float(request.form['moi'])
        tenki= int(request.form['tenki'])
        shitsudo= float(request.form['sitsu'])
        my_func.sql_data_send(userid,userpass,SQLserver_port,SQLserver_host,database_name,weight_after,weight_before,contents,time,moisture,tenki,shitsudo)
        data=my_func.sql_data_get(userid,userpass,SQLserver_port,SQLserver_host,database_name)
        posts=[]
        for d in reversed(data):
            posts.append({
              'date' : str(d[0]),
              'training' : str(d[3]),
              'bweight' : str(d[1]),
              'aweight' : str(d[2]),
              'dehydrateval' : str(d[4]),
              'dehydraterate' : str(d[5]),
              'intake' : str(d[6]),
              'period' : str(d[7])
            })

        return render_template('result.html', title='My Title', user=userid, posts=posts)
    except:
        return 'NG'

# administration page
@app.route("/admin")
def admin_entry():
    html = render_template('admin_index.html')
    return html

@app.route("/adminwindow", methods=["POST"])
def admin_window():
    userid = request.form['user']
    userpass = request.form['pass']
    administrator=['azumi']
    
    print('ID:{} ADMINLOGIN '.format(userid))
    if userid in administrator:
        print('Success')
        return render_template('adminwindow.html')
    else:
        print('Fail')
        return 'you are not an administrator'


















if __name__ == "__main__":
    app.run(debug=False, host=server_host, port=server_port, threaded=True)