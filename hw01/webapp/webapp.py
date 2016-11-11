from flask import Flask, render_template, send_file, request, redirect, url_for
import sys
import os.path

# process_queries module has to be added manually to path before import. IDE may complain about it, just ignore it.
# Be careful that following line keeps on pointing to homework 1 root directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import process_queries
from query_processing import process_query

app = Flask(__name__)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    query = None
    query=request.args.get("search_form_input_homepage")
    if query!=None:
        index = process_queries.load_index()
        recipes=None
        #process_queries.retrieve_docs_contents(process_queries.process_query(index, query))
        #Funzioni per cercare e insertare le ricetti in recipes
        return render_template('show_recipes.html', entries=entries)
    return send_file('index.html')
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')