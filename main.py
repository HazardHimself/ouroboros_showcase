from flask import Flask, render_template, request, jsonify
import functions as functions
import ouroboros as ouroboros
import pathlib

from datetime import datetime

'''
# Only use if sv_debug package and utilities are available.
import sv_utils.sv_debug as sv_debug
if sv_debug.DEBUG_MODE:
    for i in sv_debug.get_imported_modules():
        sv_debug.debug_decorate_functions(module=i, decoration=sv_debug.debug_measure_speed)
'''

# -----

app = Flask(__name__)

available_panes = ouroboros.get_available_panes()
functions_found = ouroboros.inspect_function_file(functions)
python_to_exec_001 = ouroboros.build_route_pane(available_panes=available_panes)
python_to_exec_002, js_to_write = ouroboros.build_process_requirements(list_of_functions=functions_found)

python_to_exec = python_to_exec_001.union(python_to_exec_002)

ouroboros.write_js_file(lines_to_write=js_to_write)
for line in python_to_exec: 
    exec(line)

@app.route('/', methods=['GET', 'POST'])
def index(): return render_template('index.html', available_panes = available_panes)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='localhost', port='5000')