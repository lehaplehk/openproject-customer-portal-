from flask import Blueprint
from flask import Flask
from flask import request, jsonify, send_file
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_cors import CORS, cross_origin
import env
import os


aut_api = Blueprint("aut", __name__)

def CheckAutohorizaztion(token):
    headers = {'Authorization': "Bearer "+token}
    response = dbentities.AccountProfile(headers)
    return response
    
@aut_api.route('/logout', methods=['GET'])
def logout():
    try:
        session.modified = True
        session.pop('mail', None)
        session.pop('password', None)
        session.pop('expires_in', None)
        session.pop('access_token', None)
        session.pop('refresh_token', None)
        session.pop('username', None)
        session.pop('login', None)
        return redirect(url_for("signin"))
    except Exception as error:
        ErorLog(error)
        return redirect(url_for("signin"))


#Autorization
@aut_api.route('/account/signin', methods=[ 'POST'])
def login():
    session.modified = True
    session.pop('username', None)
    session.pop('password', None)
    session.pop('expires_in', None)
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    login = request.form['login'].replace(" ","")
    login = login.replace(" ","")
    session['username'] = login
    session['login'] = login 
    response = dbentities.signin(session.get('username'),request.form['password'])
    if response == 404:
        return render_template('error/401.html'), 404
    if response == 403:
        return render_template('error/403.html'), 403
    else:
        if 'ban' in dbentities.GetUserRight(login):
            return render_template('error/ban.html'), 403
        req = response
        session.modified = True
        #session['access_token'] = req['access_token'].decode("utf-8")
        session['access_token'] = req['access_token']
        session['expires_in'] = req['expires_in']
        session['refresh_token'] = req['refresh_token']
        session['token_type'] = req['token_type']
        req = request.args
        if 'redirect' in req:
            return redirect(req['redirect'])
        return redirect(url_for("storage"))


@aut_api.route('/account/user/img', methods=['GET'])
def account_user_img():
    req = request.args
    if 'access_token' in session:
        response = CheckAutohorizaztion(session.get('access_token'))
        if response == 401:
            return {"status": 403,"message":'Нет доступа'},403
        return send_file(autfunc.GetUserPhoto(response.login)[0]), 200
    return {"status": 401,"message":'Не авторизован'},401

@aut_api.route('/account/user/shared/img', methods=['GET'])
def account_user_shared_img():
    req = request.args
    if 'access_token' in session:
        response = CheckAutohorizaztion(session.get('access_token'))
        if response == 401:
            return {"status": 403,"message":'Нет доступа'},403
        return send_file(autfunc.GetUserPhoto(req['user'])[0]), 200
    return {"status": 401,"message":'Не авторизован'},401

@aut_api.route('/account/profile', methods=['GET'])
def account_profile():
    req = request.args
    if 'access_token' in session:
        response = CheckAutohorizaztion(session.get('access_token'))
        if response == 401:
            return {"status": 403,"message":'Нет доступа'},403
        return render_template("account.html",
        login=response.login)
    return render_template('error/401.html'), 401

@aut_api.route('/account/profile/changepass', methods=['POST'])
def account_profile_changepass():
    req = request.args
    if 'access_token' in session:
        response = CheckAutohorizaztion(session.get('access_token'))
        if response == 401:
            return {"status": 403,"message":'Нет доступа'},403
        js = request.get_json()
        return autfunc.ChangeUserPassword(response.login,js['old_pass'],js['new_pass'])
    return {"status": 401,"message":'Не авторизован'},401

@aut_api.route('/account/profile/upload/photo', methods=['POST'])
def account_actions_uploadphoto():
    req = request.args
    if 'access_token' in session:
        response = CheckAutohorizaztion(session.get('access_token'))
        if response == 401:
            return {"status": 403,"message":'Нет доступа'},403
        files = request.files.getlist("file")
        for file in files:
            file.save(storeg+response.login+"/profile.jpg")
            if os.path.getsize(storeg+response.login+"/profile.jpg") > 3145728:
                os.remove(storeg+response.login+"/profile.jpg")
                return {"status": 400,"message":'Файл больше 3 мб'},400
        return redirect(url_for("aut.account_profile"))
    return {"status": 401,"message":'Не авторизован'},401
        