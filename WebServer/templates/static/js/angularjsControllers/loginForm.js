/**
 * Created by varun on 17/02/15.
 */
function setSuccessClass(group) {
  group.attr('class', "control-label has-feedback form-group has-success");
}

function setEmptyClass(group) {
  group.attr('class', "control-label has-feedback ");
}

function setWarningClass(group) {
  group.attr('class', "form-group has-warning has-feedback");
}

function setErrorClass(group) {
  group.attr('class', "control-label has-feedback form-group has-error");
}

function setEmptyIcon(statusIcon) {
  statusIcon.attr('class', "");
}

function setSuccessIcon(statusIcon) {
  statusIcon.attr('class', "glyphicon glyphicon-ok form-control-feedback");
}

function setErrorIcon(statusIcon) {
  statusIcon.attr('class', "glyphicon glyphicon-alert form-control-feedback");
}

function setWarningIcon(statusIcon) {
  statusIcon.attr('class', "glyphicon glyphicon-warning-sign form-control-feedback");
}

function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test($email);
}

var app = angular.module("graphfusion", []);

app.controller("loginFormCtrl", function ($scope) {

  $scope.loginMessage = function () {
    if ($scope.username.length < 1) {
      return "Please enter username."
    }
    if ($scope.password.length < 1) {
      return "Please enter password."
    }
    return "";
  };
});
