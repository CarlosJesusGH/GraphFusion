/**
 * Created by varun on 24/03/15.
 */

function successAlert(message) {
  alertify.success("<center style='font-size: medium'><i class='fa fa-lg fa-check-circle'></i>  " + message + "</center>");
}

function errorAlert(message) {
  alertify.error("<center style='font-size: medium'><i class='fa fa-lg fa-exclamation-triangle'></i>  " + message + "</center>");
}

// function to log including a timestamp
function log_timestamp(location, message) {
  var now = new Date();
  console.log(now.toUTCString() + ". " + location + ". " + message);
}