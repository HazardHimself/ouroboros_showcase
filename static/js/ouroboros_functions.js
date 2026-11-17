import('./functions.js')

import('./shared_functions.js')

function process_easy_return(){
	var submission = snapshot_page_data()
	$.ajax({
		url: '/ouroboros_process_easy_return',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(submission),
		success: function(response) {process_easy_return_return(response)},
		error: function(error) {error_handler(error)},
	})
}
