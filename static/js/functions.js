function ExecPython(pythonCommand) {
    var request = new XMLHttpRequest()
    request.open("GET", "/" + pythonCommand, true)
    request.send()
}

function error_handler(error) {
    console.log(error);
    let resp = error.responseText;
    const regex = RegExp('<title>(.+?)<\\\/title>', 'gms')
    re = regex.exec(resp)
    alert(re[1])
}

function load_pane(pane_name, pane_container) {
    $.get( '/'+pane_name, function( data ) {
        $( "#"+pane_container ).html( $("#"+pane_container).html() + data );
    });
    return true
}

function empty_container(container_name) {
    container_to_empty = document.getElementById(container_name)
    container_parent = container_to_empty.parentNode
    replacement = document.createElement(container_to_empty.nodeName)
    container_to_empty.remove()
    replacement.id = container_name
    console.log(container_parent.appendChild(replacement))
}

function empty_container_in_place(container_name) {
    container_to_empty = document.getElementById(container_name)
    container_to_empty.innerHTML = '';
}

function show_pane(pane_name) {
    document.getElementById(pane_name).style.removeProperty('display')
}

function unload_pane(pane_name) {
    document.getElementById(pane_name).remove()
}

function double_duty_pane_load(pane_name, container) {
    empty_container_in_place(container)
    load_pane(pane_name, container)
}