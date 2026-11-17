import pathlib, os, sys
from flask import Flask, render_template, request, jsonify
import json
import types
import inspect

# Ouroboros Pane Handler - Start
# Sets up route handlers based off existing templates in the templates folder.

def get_available_panes():
    available_panes = []
    for i in pathlib.Path('templates').iterdir(): 
        item_name = i.stem
        if item_name.startswith('pane_'):
            available_panes.append(item_name)

    return available_panes

def build_route_pane(available_panes: list):
    python_to_exec = set()
    for pane in available_panes:
        exec_command = f"@app.route('/ouroboros_{pane}', methods=['POST'])\ndef ouroboros_{pane}():\n\tsubmission=request.get_json()\n\tprint('[',datetime.now().strftime('%Y-%m-%d - %H:%M:%S'),'] - Received Ouroboros Request for {pane} with data: '+ str(submission))\n\treturn render_template('{pane}.html', submission=submission)"
        python_to_exec.add(exec_command)

    return python_to_exec
        
# Ouroboros Pane Handler - End

# Ouroboros Function Handler - Start
# Ouroboros handles functions in pythons by hitting routes. Routes need to exist and be hit via javascript.
# Or, more accurately and easily, hit by AJAX.
# And in order to do that, we need a few functions to make our lives easier.
def write_js_file(lines_to_write: list):
    PARENT_DIRECTORY = os.path.dirname(os.path.abspath(inspect.stack()[-1].filename))
    JS_FILEPATH = f'{PARENT_DIRECTORY}{os.sep}static{os.sep}js{os.sep}'
    pathlib.Path(JS_FILEPATH).mkdir(parents=True, exist_ok=True)

    prepend_lines = [
        '\nfunction ExecPython(pythonCommand) {\n\tvar request = new XMLHttpRequest() \n\trequest.open("GET", "/" + pythonCommand, true) \n\trequest.send()\n}\n',
        "\nfunction error_handler(error) {\n\tconsole.log(error);\n\tlet response = error.responseText;\n\tconst regex = RegExp('<title>(.+?)<\\/title>', 'gms');\n\tre = regex.exec(response);\n\talert(re[1]);\n}\n",
        '\nfunction form_to_object(form_id) { let form_object = Object.values(document.getElementById(form_id)).reduce((obj, field) => { if (field.name) { if ((field.type == "radio") || (field.type == "checkbox")) {if (field.checked) {obj[field.name] = field.value} } else {obj[field.name] = field.value} }; return obj }, {}); return form_object }\n',
        '\nfunction snapshot_page_data() {\n\tvar forms_collection = document.getElementsByTagName("form");\n\t\tlet page_snapshot = {}\n\t\tfor(var i=0; i < forms_collection.length; i++) {\n\tlet form_id = forms_collection[i].id\n\tpage_snapshot[form_id] = form_to_object(form_id)\n\t}\n\treturn page_snapshot\n}\n',
        "\nfunction load_pane(pane_name, pane_container, request_body = {}) {\n\tlet request_data = {\n\t\trequest_body: request_body,\n\t\tpage_snapshot: snapshot_page_data() \n\t};\n\t$.ajax({\n\t\turl: '/'+pane_name,\n\t\ttype: 'POST',\n\t\tcontentType: 'application/json',\n\t\tdata: JSON.stringify(request_data),\n\t\tsuccess( data ) {\n\t\t\t$( '#'+pane_container ).html( $('#'+pane_container).html() + data );\n\t\t}\n\t});\n}\n",
        "\nfunction empty_container(container_name) {\n\tlet container_to_empty = document.getElementById(container_name) \n\treplacement = document.createElement(container_to_empty.nodeName) \n\tcontainer_to_empty.remove() \n\treplacement.id = container_name \n}\n",
        "\nfunction empty_container_in_place(container_name) {\n\tcontainer_to_empty = document.getElementById(container_name) \n\tcontainer_to_empty.innerHTML = ''; \n}\n",
        "\nfunction show_pane(pane_name) {\n\tdocument.getElementById(pane_name).style.removeProperty('display')\n}\n",
        "\nfunction unload_pane(pane_name) {\n\tdocument.getElementById(pane_name).remove()\n}\n",
        "\nfunction double_duty_pane_load(pane_name, container, request) { \n\tvalidate_check(self) \n\tempty_container_in_place(container) \n\tload_pane(pane_name, container, request) \n}\n",
        "\nfunction validate_check(self) {\n\tself.value = self.checked\n}\n"
    ]

    with open(f'{JS_FILEPATH}shared_functions.js', 'w') as js_file:
            for line in prepend_lines:
                js_file.write(line)
            js_file.close()

    ouroboros_prepend = [
        "import('./functions.js')\n",
        "\nimport('./shared_functions.js')\n"
    ]

    lines_to_write = ouroboros_prepend + lines_to_write

    with open(f'{JS_FILEPATH}ouroboros_functions.js', 'w') as js_file:
        for line in lines_to_write:
            js_file.write(line)
        js_file.close()

def build_route_process_js(function_to_handle: str):
    generic_request = [
        '\nfunction '+function_to_handle+'(){',
        '\tvar submission = snapshot_page_data()',
        '\t$.ajax({\n'
        "\t\turl: '/ouroboros_"+function_to_handle+"',",
        "\t\ttype: 'POST',",
        "\t\tcontentType: 'application/json',",
        "\t\tdata: JSON.stringify(submission),",
        "\t\tsuccess: function(response) {"+function_to_handle+"_return(response)},",
        "\t\terror: function(error) {error_handler(error)},",
        "\t})",
        "}\n"]
    string_request = '\n'.join(generic_request)
    return string_request

def build_route_process_python(function_to_handle: str):
    generic_process_route = [
        f"@app.route('/ouroboros_{function_to_handle}', methods=['POST'])",
        f"def ouroboros_{function_to_handle}():",
        f"\tsubmission=request.get_json()",
        f"\tprint('[',datetime.now().strftime('%Y-%m-%d - %H:%M:%S'),'] - Received Ouroboros Request for {function_to_handle} with data: '+ str(submission))",
        f"\tfunction_returned_value = functions.{function_to_handle}(submission=submission)",
        f"\trequest_returned_value = jsonify(returned_value=function_returned_value)",
        f"\treturn request_returned_value"
    ]
    exec_command = '\n'.join(generic_process_route)
    return exec_command
    
def build_process_requirements(list_of_functions: set):
    python_to_exec = set()
    js_to_write = []
    for function_handler in list_of_functions:
        if function_handler.startswith('process_'):
            python_to_exec.add(build_route_process_python(function_handler))
            js_to_write.append(build_route_process_js(function_handler))

    return python_to_exec, js_to_write

def inspect_function_file(function_file: types.ModuleType):
    functions_found = set()
    for name in dir(function_file):
        found_function = getattr(function_file, name)
        if isinstance(found_function, types.FunctionType):
            functions_found.add(name)
    return functions_found

# Ouroboros Function Handler - End