#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

from pymongo import MongoClient

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/mongo/')
@app.route('/mongo/<id>')
def mongo():
    client=MongoClient('127.0.0.1',27017)

    # connect to database
    db=client.mv

    data=db.info.find({}).limit(10)
    #data=db.jav.find({"fullname":/本田"/})

    return render_template('mongo.html', info=data)

if __name__ == "__main__":
    app.run()