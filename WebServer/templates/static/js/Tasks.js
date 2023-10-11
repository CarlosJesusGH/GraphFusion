/**
 * Created by varun on 11/05/15.
 */


var runningTasksList;
var taskNameValue = 'taskName';


function displayTaskView($task_id, $div_for_display) {
  $.ajax({
    url: '/TaskFactory/task/' + $task_id.toString() + "/",
    type: 'GET',
    data: {},
    success: function (data) {
      $div_for_display.html(data);
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while retrieving view for task: " + xhr.responseText);
    }
  });
}

function getSuccessfulTasksForUser($task_type, $task_list_div) {
  $.ajax({
    url: '/TaskFactory/Success/' + $task_type.toString() + "/",
    type: 'POST',
    data: {},
    success: function (data) {
      $task_list_div.html(data);
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while getting finished tasks: " + xhr.responseText);
    }
  });
}

function getTasksForUser($task_type, $task_list_div) {
  $.ajax({
    url: '/TaskFactory/' + $task_type.toString() + "/",
    type: 'POST',
    data: {},
    success: function (data) {
      $task_list_div.html(data);
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while getting finished tasks: " + xhr.responseText);
    }
  });
}

function getAndAppendFinishedTasksForUser($task_type, $task_list_div) {
  $.ajax({
    url: '/TaskFactory/Success/' + $task_type.toString() + "/",
    type: 'POST',
    data: {},
    success: function (data) {
      $task_list_div.append(data);
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while getting finished tasks: " + xhr.responseText);
    }
  });
}

function deleteTask($task_id, callback) {
  $.ajax({
    url: '/TaskFactory/delete/' + $task_id.toString() + "/",
    type: 'POST',
    data: {},
    success: function (data) {
      successAlert(data);
      callback();
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while deleting task: " + xhr.responseText);
    }
  });
}

function terminateTask($task_id, callback) {
  $.ajax({
    url: '/TaskFactory/terminate-task/' + $task_id.toString() + "/",
    type: 'POST',
    data: {},
    success: function (data) {
      successAlert(data);
      callback();
    },
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log('ERRORS: ' + textStatus);
      errorAlert("Error occurred while deleting task: " + xhr.responseText);
    }
  });
}

function getOldTasks() {
  var oldTasks = [];
  for (var i = 0; i < runningTasksList.items.length; i++) {
    oldTasks.push(runningTasksList.items[i].values()['taskName']);
  }
  return oldTasks;
}

function removeTasks(tasksToDelete) {
  for (var j = 0; j < tasksToDelete.length; j++) {
    runningTasksList.remove(taskNameValue, tasksToDelete[j]);
    successAlert("Task " + tasksToDelete[j] + " successfully completed.")
    // Check if the page is the dashboard page
    if (document.getElementById("dashboard-results-html")) {
      navigateTo("/dashboard/");
    }
  }
}

function addNewTasksToList(tasksToAdd) {
  for (var i = 0; i < tasksToAdd.length; i++) {
    runningTasksList.add({
      taskName: tasksToAdd[i]
    });
  }
}

function refreshRunningTasks() {
  Pace.ignore(function () {
    $.ajax({
      url: '/TaskFactory/running-tasks/',
      type: 'POST',
      data: {},
      success: function (data) {
        var currentRunningTasks = JSON.parse(data);
        var oldTasks = getOldTasks();
        removeTasks($(oldTasks).not(currentRunningTasks).get());
        addNewTasksToList($(currentRunningTasks).not(oldTasks).get());
        try {
          // cgh_20220408: I deleted this because it was spoiling the "#previouslyComputedTasksList" selector behavior
          // console.log("refreshRunningTasks-success-try");
          // updateTaskList();
        } catch (e) {

        }
      },
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
      },
      error: function (xhr, textStatus, errorThrown) {
        console.log('ERRORS: ' + textStatus);
      }
    })
  });
  return false;
}

function initialiseRunningTasksList(tasks_list) {
  var options = {
    valueNames: [taskNameValue],
    item: '<li class="running-task-elem padding-0" style="padding: 0!important;">\
    <div class="progress padding-0" style="width:100%; height: 100%;">\
      <div class="col-sm-8 progress-bar progress-bar-striped active padding-0" role="progressbar"\
           aria-valuenow="40" aria-valuemin="0" aria-valuemax="100"\
           style="width:100%; height: 100%; padding:0; margin:0;">\
        <h6 class="taskName"></h6>\
      </div>\
    </div>\
  </li>'
  };
  runningTasksList = new List(tasks_list, options);
  refreshRunningTasks();
  setInterval(function () {
    refreshRunningTasks();
  }, 5000);
}