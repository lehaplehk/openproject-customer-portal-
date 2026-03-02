# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, jsonify, send_file
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename
import os
import json
import datetime
from datetime import datetime, timedelta, timezone
import requests
import time
import random 
import env
from aut import aut_api  

app = Flask(__name__)
app.register_blueprint(aut_api, url_prefix="/aut")

PageConf = open("./custom/page.json", 'r')
PageConf = json.load(PageConf)

@app.route('/')
def home():
    return render_template("index.html",
        CUSTOMER_PORTAL_NAME=env.CUSTOMER_PORTAL_NAME)

@app.route('/signin')
def signin():
    return render_template("aut/signin.html",
        CUSTOMER_PORTAL_NAME=env.CUSTOMER_PORTAL_NAME)



app.run(host=env.LISTEN_ADRESS, port=env.LISTEN_PORT)

