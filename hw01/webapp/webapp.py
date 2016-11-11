from flask import Flask, render_template, send_file
# from hw01 import process_queries

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')