#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, Response, render_template
import subprocess
import json
from postDataToSmartDogServer import Smart7688ToDog

HOST = '0.0.0.0'
PORT = '5000'

app = Flask(__name__, static_folder='src')


@app.route("/api/sensors")
def read_serial():
    s= Smart7688ToDog()
    out = s.parserSensorValue()
    s.capDisplayImg()

#    try:
#        out = json.dumps(eval(out.strip()))
#    except Exception, e:
#        out = json.dumps({'stdout': out})

    return Response(
        response=json.dumps(out),
        mimetype="application/json",
        status=200
    )

@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
