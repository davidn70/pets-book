from flask import Flask, render_template, request, redirect
from flask import send_from_directory
import uuid
import base64
import json

BUCKET_NAME = ''
PROJECT_NAME = ''

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    print("Hello World")
    return "hello world"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)