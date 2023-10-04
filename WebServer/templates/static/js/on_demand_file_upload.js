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
  // log
  console.log("setUpOnDemandFileUpload()");
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
  console.log("uploadFile(), files.length:", files.length, "files:", files);
  event.stopPropagation();
  event.preventDefault();

  //TODO: START A LOADING SPINNER HERE
  

  
  // Upload the files to the server. Use a different FileReader object for each file. This is because the onloadend function is called asynchronously. If we use the same FileReader object for all files, then the onloadend function will be called only after the last file is read. This will cause the same file to be uploaded multiple times.
  for (var i=0; i<files.length; i++) {
    var reader = new FileReader();
    reader.onloadend = (function(file) {
      return function(evt) {
        createListItem(evt, file)
      };
    })(files[i]);
    reader.readAsText(files[i]);
  }
  // Reset the file input box
  $("#loadNetworkModal").modal('toggle');
}

function createListItem(evt, file) {
  // console.log(evt.target.result)
  // console.log(file.name);
  if (evt.target.readyState == FileReader.DONE) { // DONE == 2
    var file_content = evt.target.result;
    var file_name = file.name;
    // Remove the file extension
    file_name = file_name.substring(0, file_name.lastIndexOf('.'));
    // Remove any non-alphanumeric characters and spaces. Keep only underscores.
    file_name = file_name.replace(/[^a-zA-Z0-9_]/g, "");
    loadNetworkFile(file_name, file_content);
    fileUploadForm[0].reset();
    updateNetworks();
  }
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