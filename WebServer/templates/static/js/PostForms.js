/**
 * Created by varun on 07/05/15.
 */

function postForm(form, url, successMessage, errorMessage) {
  Pace.track(function () {
    $.ajax({
      url: url,
      type: 'POST',
      data: {
        'data': JSON.stringify(form.serializeArray())
      },
      success: function (_) {
        successAlert(successMessage);
      },
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
      },
      error: function (xhr, textStatus, errorThrown) {
        console.log('ERRORS: ' + textStatus);
        errorAlert(errorMessage + ": " + xhr.responseText);
      }
    });
  });
}