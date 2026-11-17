
function ExecPython(pythonCommand) {
	var request = new XMLHttpRequest() 
	request.open("GET", "/" + pythonCommand, true) 
	request.send()
}

function error_handler(error) {
	console.log(error);
	let response = error.responseText;
	const regex = RegExp('<title>(.+?)<\/title>', 'gms');
	re = regex.exec(response);
	alert(re[1]);
}

function form_to_object(form_id) { let form_object = Object.values(document.getElementById(form_id)).reduce((obj, field) => { if (field.name) { if ((field.type == "radio") || (field.type == "checkbox")) {if (field.checked) {obj[field.name] = field.value} } else {obj[field.name] = field.value} }; return obj }, {}); return form_object }

function snapshot_page_data() {
	var forms_collection = document.getElementsByTagName("form");
		let page_snapshot = {}
		for(var i=0; i < forms_collection.length; i++) {
	let form_id = forms_collection[i].id
	page_snapshot[form_id] = form_to_object(form_id)
	}
	return page_snapshot
}

function load_pane(pane_name, pane_container, request_body = {}) {
	let request_data = {
		request_body: request_body,
		page_snapshot: snapshot_page_data() 
	};
	$.ajax({
		url: '/'+pane_name,
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(request_data),
		success( data ) {
			$( '#'+pane_container ).html( $('#'+pane_container).html() + data );
		}
	});
}

function empty_container(container_name) {
	let container_to_empty = document.getElementById(container_name) 
	replacement = document.createElement(container_to_empty.nodeName) 
	container_to_empty.remove() 
	replacement.id = container_name 
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

function double_duty_pane_load(pane_name, container, request) { 
	validate_check(self) 
	empty_container_in_place(container) 
	load_pane(pane_name, container, request) 
}

function validate_check(self) {
	self.value = self.checked
}
