/**
 * Created by varun on 23/02/15.
 */

var networkNameBox;
var networkList;
var fileUploadForm;
var networkFiles = [];
var fileInput;
var csrf_token = getCsrfToken();
var files = [];
var loadedNetworksList;
var number_of_networks_per_page;

function setUpOnDemandFileUpload(fileInputHtml, submitButton, networkName, networkListUL, fileUploadFormHtml) {
  fileInput = fileInputHtml;
  submitButton.on('click', uploadFile);
  fileInput.on('change', prepareUpload);
  networkList = networkListUL;
  networkNameBox = networkName;
  fileUploadForm = fileUploadFormHtml;
  number_of_networks_per_page = Math.floor(($(window).height() * .3 ) / 40) - 1;
  var options = {
    valueNames: ['name'],
    item: '<li><h3 class="name"></h3></li>',
    page: number_of_networks_per_page,
    plugins: [ListPagination({})]
  };
  loadedNetworksList = new List('loadedNetworksList', options);
  hidePageNumbers();
}

function getHttpPage(theUrl) {
  if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  }
  else {// code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      return xmlhttp.responseText;
    }
  };
  xmlhttp.open("GET", theUrl, false);
  xmlhttp.send();
}


function loadNetworkFile(name, file_content) {
  addNetworkToList(name);
  networkFiles.push([name, file_content]);
}

function uploadFile(event) {
  console.log("uploadFile()", files);
  event.stopPropagation();
  event.preventDefault();

  //TODO: START A LOADING SPINNER HERE
  var read = new FileReader();
  for (var i = 0; i < files.length; i++) {
    // NOTE_CGH_202110: this was changed to make the code work with not-text-based networks
    console.log("files[i]: ", files[i]);
    // console.log("files[i]['name']: ", files[i]["name"]);
    // flag:newtasktemplate - change the following block ONLY in case networks come with a different format/extension
    if (files[i]["name"].includes(".edgelist") || files[i]["name"].includes(".txt") || files[i]["name"].includes(".csv") || files[i]["name"].includes(".sc")) {
      console.log("readAsText");
      read.readAsText(files[i]);
    } else{
      // console.log("readAsArrayBuffer");
      // read.readAsBinaryString(files[i]);
      // read.readAsArrayBuffer(files[i]);
      console.log("readAsText");
      read.readAsText(files[i]);
    }
    read.onloadend = function () {
      var name = networkNameBox.val();
      loadNetworkFile(name, read.result);
      fileUploadForm[0].reset();
      updateNetworks();
    }
  }
  $("#loadNetworkModal").modal('toggle');
}

function showPageNumbers() {
  var pages = $("#pages-numbers");
  pages.show();
}

function hidePageNumbers() {
  var pages = $("#pages-numbers");
  pages.hide();
}

function prepareUpload(event) {
  console.log("prepareUpload()", event.target.files);
  files = event.target.files;
}

function addNetworkToList(networkName) {
  //networkList.append("<li  draggable='true'><a>" + networkName + "</a></li>");
  loadedNetworksList.add({
    name: networkName.toString()
  });
  if (loadedNetworksList.items.length > number_of_networks_per_page) {
    showPageNumbers();
  }
}

function updateNetworkNamesInList(list) {
  for (var i in networkFiles) {
    list.append("<option value=\"" + i + "\">" + networkFiles[i][0] + "</option>");
  }
}