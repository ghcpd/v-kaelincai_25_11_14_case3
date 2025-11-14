from flask import Flask, send_from_directory, render_template_string
import os
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static','index.html')

@app.route('/<path:path>')
def static_serve(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(port=3000)
