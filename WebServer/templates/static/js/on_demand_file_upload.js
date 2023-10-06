/**
 * Created by varun on 23/02/15.
 */

var networkNameBox;
var networkList;
var fileUploadForm;
var networkFiles = [];
var networkFilesUrl = [];
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
  console.log("uploadFile(), files.length:", files.length, "files:", files);
  event.stopPropagation();
  event.preventDefault();
  //TODO: START A LOADING SPINNER HERE
  for (var i=0; i<files.length; i++) {
    var reader = new FileReader();
    reader.onload = (function(file) { // reader.onloadend
      console.log("onload");
      return function(evt) {
        uploadFileCreateListItem(evt, file)
      };
    })(files[i]);
    reader.readAsText(files[i]);
  }
  // Reset the file input box
  $("#loadNetworkModal").modal('toggle');
}

function uploadFileCreateListItem(evt, file) {
  // console.log("evt.target.result", evt.target.result)
  // console.log("file.name", file.name);
  if (evt.target.readyState == FileReader.DONE) { // DONE == 2
    var file_content = evt.target.result;
    var file_name = file.name;
    // Remove the file extension
    file_name = file_name.substring(0, file_name.lastIndexOf('.'));
    // Remove any non-alphanumeric characters and spaces. Keep only underscores.
    file_name = file_name.replace(/[^a-zA-Z0-9_]/g, "");
    // Check if the file is too big, more than 100MB
    // if (file_content.length > 100000000) {
    //   alert("File is too big! Maximum allowed size is 100MB.");
    //   return false;
    // }
    // Check if file is already loaded
    if (networkFiles.length > 0) {
      for (var j=0; j<networkFiles.length; j++) {
        if (networkFiles[j][0] == file_name) {
          alert("File is already loaded!");
          return false;
        }
      }
    }
    // Send the file to the server
    console.log("uploadFileCreateListItem() - sending file to server");
    // var formData = new FormData();
    // formData.append('file', file);
    // formData.append('name', file_name);
    var data = {'Networks': []};
    data.Networks.push([file_name, file_content]);
    // console.log("data", data);
    // console.log("file_name", file_name);  
    $.ajax({
      url: '/dashboard/upload_network',
      type: 'POST',
      data: {
        'data': JSON.stringify(data),
      },
      // processData: false,
      // contentType: false,
      success: function (data) {
        console.log('success');
        var jsonparams = JSON.parse(data);
        var msg = jsonparams.msg;
        successAlert(msg);
        // If everything is ok, load the file
        loadNetworkFile(file_name, file_content);
        // Reset the file input box
        fileUploadForm[0].reset();
        updateNetworks();
      },
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
      },
      error: function (xhr, textStatus, errorThrown) {
        console.log('ERRORS: ' + textStatus);
        errorAlert("Error occurred while uploading file: " + xhr.responseText);
      }
    });
  }
}

function download_networks() {
  // Make a GET request to the server to download the networks
  $.ajax({
    url: '/dashboard/download_networks',
    type: 'GET',
    success: function (data) {
      var jsonparams = JSON.parse(data);
      var networks = jsonparams.networks;
      for (var i=0; i<networks.length; i++) {
        var network = networks[i];
        var name = network[0];
        var file_content = network[1];
        loadNetworkFile(name, file_content);
      }
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while downloading networks: " + xhr.responseText);
    }
  });
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


