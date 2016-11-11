from flask import Flask, render_template, send_file
import sys
import os.path

# process_queries module has to be added manually to path before import. IDE may complain about it, just ignore it.
# Be careful that following line keeps on pointing to homework 1 root directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import process_queries

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')