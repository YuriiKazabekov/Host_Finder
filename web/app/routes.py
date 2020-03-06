from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, DeleteForm
from app.models import User
from backuper import *



################################################################

import mysql.connector

import csv


#conn = mysql.connector.connect(host='localhost',
#                                      database='myapp',
#                                      user='myapp',
#                                      password='Mad_H0rse',
#                                          autocommit=True)
#cursor = conn.cursor()
    
#df = []
################################################################
import sqlite3
sqlite_file = '/home/appliance/venv/web/app.db'  
################################################################



@app.route('/')
@app.route('/index')
@login_required
def index():
###############################################################################
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()
########################################################################################
    text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address ORDER BY fdb.switch_IP'
    cursor.execute(text_sql)
    #df = pd.DataFrame(cursor.fetchall())
    #df.columns = ["Mac-address", "Switch IP", "Port number", "Vlan", "Host IP", "Host name", "VOIP account", "Phone number", "VOIP agent type", "Last check"]
    #df.fillna(value=pd.np.nan, inplace=True)
    #return render_template('index.html', df=[df.to_html(index=False, classes='data' ,na_rep = ' ', justify = 'center')], titles=df.columns.values)
    df = cursor.fetchall()
    with open('/home/appliance/venv/web/app/file/output.csv','w') as result_file:
        wr = csv.writer(result_file)
        wr.writerows(df)
########################################################################################################        
    cursor.close()
    conn.close()
########################################################################################################     
    return render_template('index.html', df=df)
##################################################################################

@app.route('/')
@app.route('/index2')
@login_required
def index2():
    if current_user.role == 'admin':
        return render_template('index2.html')
    else:
        return redirect(url_for('index'))


####
####
@app.route('/process_data_2/', methods=['GET','POST'])
@login_required
def doit2():
    show_result= []
    backup(show_result)
    print(show_result)
    return render_template('index2.html', show_result=show_result)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


'''@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)'''
#######################################################################################
#Admin panel    
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    #if current_user.get_id() == '1' or current_user.get_id() == '2':
    if current_user.role == 'admin':
    #if 0 == 0 :
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, role=form.role.data)# email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('admin'))
        form2 = DeleteForm()
        if form2.validate_on_submit():
            user = User(username=form2.username.data)# email=form.email.data)
            mystring = str(user)
            ##########
            keyword = '>'
            before_keyword, keyword, after_keyword = mystring.partition(keyword)
            mystring = before_keyword
            keyword = '<User '
            before_keyword, keyword, after_keyword = mystring.partition(keyword)
            mystring = after_keyword
            print(mystring)
            ############
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor() 
            c.execute('DELETE FROM user WHERE username ="{}" '.format(mystring))
            conn.commit()    
            conn.close()
            
            flash('Congratulations, you are delete user!')
            return redirect(url_for('admin'))
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor() 
        #c.execute("SELECT * FROM user")
        c.execute("SELECT id, username, role FROM user")
        rows = c.fetchall()
        
        
        
        return render_template('admin.html', title='Admin', form=form,form2=form2, rows=rows)    
    else:
        pass
    
    
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)# email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





@app.before_request
def load_users():
    guser = current_user.get_id() # return username in get_id()
    cuser = current_user
    try:
        urole = current_user.role
        print(urole)
    except AttributeError: 
        pass
    #print(guser)
    #print(cuser)
    
    #conn = sqlite3.connect(sqlite_file)
    #c = conn.cursor() 
    #c.execute('SELECT  role FROM user WHERE id = "{}"'.format(guser))
    #role = c.fetchall()
    #print(role)
############################################################################


@app.route('/process_data/', methods=['GET','POST'])
@login_required
def doit():
###############################################################################
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()
########################################################################################
    #print("Posted data : {}".format(request.form))
    sval = request.form['SelectKey']
    print(sval)
    if len(sval)<35:
        
        try:
            text_sql = 'SELECT fdb.mac_address, fdb.switch_IP, fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address AND fdb.mac_address = "{}" OR select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "%{}%" OR select_result.mac_address = fdb.mac_address AND fdb.vlan_ID = "{}" OR select_result.mac_address = fdb.mac_address AND fdb.switch_IP = "{}" OR select_result.mac_address = fdb.mac_address AND select_result.phone_number = "{}" OR select_result.mac_address = fdb.mac_address AND select_result.hostname LIKE "%{}%" OR select_result.mac_address = fdb.mac_address AND select_result.VOIP_agent LIKE "%{}%" OR select_result.mac_address = fdb.mac_address AND select_result.user_account LIKE "%{}%"'.format(sval, sval, sval, sval , sval, sval, sval, sval)
            cursor.execute(text_sql)
            df = cursor.fetchall()
            with open('/home/appliance/venv/web/app/file/output.csv','w') as result_file:
                wr = csv.writer(result_file)
                wr.writerows(df)
            return render_template('index.html', df=df)

        #df = pd.DataFrame(cursor.fetchall())
        #df.columns = ["Mac-address", "Switch IP", "Port number", "Vlan", "Host IP", "Host name", "VOIP account", "Phone number", "VOIP agent type", "Last check"]
       # df.fillna(value=pd.np.nan, inplace=True)
       # return render_template('index.html', df=[df.to_html(index=False, classes='data' ,na_rep = ' ', justify = 'center')], titles=df.columns.values)
        except:
             text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address ORDER BY fdb.switch_IP'
             cursor.execute(text_sql)
             df = cursor.fetchall()
             with open('/home/appliance/venv/web/app/file/output.csv','w') as result_file:
                 wr = csv.writer(result_file)
                 wr.writerows(df)
             return render_template('index.html', df=df)

         #df = pd.DataFrame(cursor.fetchall())
         #df.columns = ["Mac-address", "Switch IP", "Port number", "Vlan", "Host IP", "Host name", "VOIP account", "Phone number", "VOIP agent type", "Last check"]
         #df.fillna(value=pd.np.nan, inplace=True)
         #return render_template('index2.html', df=[df.to_html(index=False, classes='data' ,na_rep = ' ', justify = 'center')], titles=df.columns.values)
    else:
        text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address ORDER BY fdb.switch_IP'
        cursor.execute(text_sql)
        df = cursor.fetchall()
        sval = ''
        with open('/home/appliance/venv/web/app/file/output.csv','w') as result_file:
            wr = csv.writer(result_file)
            wr.writerows(df)

        return render_template('index.html', df=df)
    sval = ''
########################################################################################################        
    cursor.close()
    conn.close()
######################################################################################################## 
@app.route('/kyiv/', methods=['GET','POST'])
@login_required
def kyiv():
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()

    text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "10.0.%" AND fdb.switch_IP LIKE "10.0.%" OR select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "10.0.%" AND fdb.switch_IP LIKE "192.%" ORDER BY fdb.switch_IP'    
    cursor.execute(text_sql)
    df = cursor.fetchall()
  
    return render_template('index.html', df=df)
     
    cursor.close()
    conn.close()
##############################################################
@app.route('/boston/', methods=['GET','POST'])
@login_required
def boston():
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()

    text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "10.10.20.%" AND fdb.switch_IP LIKE "10.10.20%" ORDER BY fdb.switch_IP'    
    cursor.execute(text_sql)
    df = cursor.fetchall()
  
    return render_template('index.html', df=df)
     
    cursor.close()
    conn.close()
##############################################################
@app.route('/moscow/', methods=['GET','POST'])
@login_required
def moscow():
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()

    text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "10.10.3%"  AND fdb.switch_IP LIKE "10.10.30%" ORDER BY fdb.switch_IP'    
    cursor.execute(text_sql)
    df = cursor.fetchall()
  
    return render_template('index.html', df=df)
     
    cursor.close()
    conn.close()
##############################################################
@app.route('/london/', methods=['GET','POST'])
@login_required
def london():
    conn = mysql.connector.connect(host='localhost',
                                      database='myapp',
                                      user='myapp',
                                      password='Mad_H0rse',
                                      autocommit=True)
    cursor = conn.cursor()

    text_sql = 'SELECT fdb.mac_address, fdb.switch_IP,fdb.port_number, fdb.vlan_ID, select_result.IP, IFNULL(select_result.hostname, "")  , IFNULL(select_result.user_account, ""), IFNULL(select_result.phone_number, ""), IFNULL(select_result.VOIP_agent, ""), fdb.time_of_adding FROM fdb, select_result WHERE select_result.mac_address = fdb.mac_address AND select_result.IP LIKE "10.10.40%" ORDER BY fdb.switch_IP'    
    cursor.execute(text_sql)
    df = cursor.fetchall()
  
    return render_template('index.html', df=df)
     
    cursor.close()
    conn.close()
##############################################################


@app.route('/getfile/', methods=['GET','POST'] )
@login_required
def export_csv():
    
    return send_file('/home/appliance/venv/web/app/file/output.csv' ,as_attachment=True, attachment_filename='output.csv')

    