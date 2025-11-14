from flask import Flask, send_from_directory, request
import argparse
import os

app = Flask(__name__, static_folder='src')

@app.route('/')
def index():
    return send_from_directory('src', 'index.html')

@app.route('/<path:path>')
def serve(path):
    return send_from_directory('src', path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=3000)
    args = parser.parse_args()
    app.run(port=args.port)
