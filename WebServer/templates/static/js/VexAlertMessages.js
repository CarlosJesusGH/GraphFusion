/**
 * Created by varun on 26/05/15.
 */

function vexErrorAlert(message) {
  vex.dialog.alert({
    message: "<div class=\"col-lg-2\"><i class=\"fa fa-exclamation-circle error-color fa-3x\"></i></div><div class=\"col-lg-10\">"
    + message + "</div><br>",
    css: {
      height: '50px !important;'
    },
    contentCSS: {height: '50px !important'}
  });
}