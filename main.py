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
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('API_KEY')

print(api_key)
#import sys  
#    if sys.argv[1] == "--new-key":
#        dbentities.GEN_KEYS()
#        app.run(host=WebConf["ip"], port=WebConf['port'])
#    if sys.argv[1] == "--start":
#        app.run(host=WebConf["ip"], port=WebConf['port'])
#    if sys.argv[1] == "--start-ssl":
#        app.run(host=WebConf["ip"], port=WebConf['port'],ssl_context=('./ssl/cert.pem', './ssl/key.pem'))