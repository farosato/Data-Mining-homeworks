from flask import Flask, render_template, send_file, request
import sys
import os.path
import time

import __init__  # update Python PATH
import hw01.process_queries as pq


app = Flask(__name__)

# has to be defined outside main, to allow queries from website
index = pq.load_index()


@app.route('/')
def root():
    query = request.args.get('query')
    if query:
        start_time = time.time()
        results = pq.retrieve_docs_contents(pq.process_query(index, str(query)))
        elapsed = time.time() - start_time
        return render_template('query_results.html', query=query, time=elapsed, results=results)
    else:
        return send_file('index.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # set debug to True to allow auto-reloading during development
