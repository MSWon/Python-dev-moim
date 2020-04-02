import os
import sys
import json

from flask import Flask, Response, request, jsonify

app = Flask (__name__)

@app.route("/add", methods=["GET"])
def index():
    num1 = request.args.get("num1")
    num2 = request.args.get("num2")
    result = int(num1) + int(num2)
    return jsonify({'num1':num1, 'num2':num2, 'add_result':result})

app.run(host='0.0.0.0', port=6006, debug=True)
