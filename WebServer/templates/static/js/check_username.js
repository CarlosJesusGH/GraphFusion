function check_username_exists(callback)
{
	var csrftoken = getCsrfToken();
	$.ajax({
	        type: 'POST',
	        url: '/check-username/',
	        data: {
	                'username': user.val()
	              },
	        beforeSend: function(xhr, settings) 
	              {
	                xhr.setRequestHeader("X-CSRFToken", csrftoken);
	              },
	        success: function(response) 
	              {
	                callback(response);
	              }
	    });
}