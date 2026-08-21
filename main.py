from flask import Flask, render_template, request, jsonify
import functions as functions

import pathlib

# -----

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index(): return render_template('index.html', available_panes = available_panes)

# I call this one the ouroboros.
# Python writing python.
def pane_handler(pane_name: str):
    exec(f"@app.route('/{pane_name}', methods=['GET'])\ndef {pane_name}(): return render_template('{pane_name}.html')")

available_panes = []

for i in pathlib.Path('templates').iterdir(): 
    item_name = i.stem
    if item_name.startswith('pane_'): available_panes.append(item_name)

for pane in available_panes: pane_handler(pane)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='localhost', port='5000')