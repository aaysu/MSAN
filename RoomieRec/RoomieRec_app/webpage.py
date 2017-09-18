from flask import Flask
from json2html import *


app = Flask(__name__)


def searchpage():
    return app.send_static_file('submit.html')


def recpage(json):
    return json2html.convert(json = json)
