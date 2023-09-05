# to create a new option with this template follow the next steps
- copy+paste folder "WebServer/a_NewTaskTemplate" and change the name for your choice
- if it's a "Properties" type of option, remove the files: NewTaskTemplateAnalysis.py, and NewTaskTemplateResult.py. Otherwise remove those containing "Properties" in the name.
- change the names for the "*Analysis.py" and "*Result.py" files and their corresponding inner class, save modified files and continue
- make a search in the new directory for the word "newtasktemplate" 
- start by openning the "settings.py" file and change every ocurrence with the corresponding substite. NOTE: the change for variables should be done using F2 in order to update all the references
- keep replacing other occurences from other files
- make a search in the whole project for the word "flag:newtasktemplate". This will show important places where you need to include a reference to the new option
- copy+paste folder "WebServer/template/a_NewTaskTemplate" and change the name for your choice
- make a search inside the new folder for the word "newtasktemplate". change the necessary references.
- delete the readme.md file in the new directory


Use the following to speed the process up:
replace 
NewTaskTemplate
and
NEW_TASK_TEMPLATE
```
NewTaskTemplateAnalysis
NEW_TASK_TEMPLATE_ANALYSIS

# models.py
from NewTaskTemplateAnalysis.settings import NEW_TASK_TEMPLATE_ANALYSIS_TASK
(NEW_TASK_TEMPLATE_ANALYSIS_TASK, NEW_TASK_TEMPLATE_ANALYSIS_TASK),

# settings.py
from NewTaskTemplateAnalysis.settings import NEW_TASK_TEMPLATE_ANALYSIS_TASK
from NewTaskTemplateAnalysis.views import get_view_for_task as NewTaskTemplateAnalysis_view, \
    delete_data_for_task as NewTaskTemplateAnalysis_delete, get_raw_data_for_task as NewTaskTemplateAnalysis_result
NEW_TASK_TEMPLATE_ANALYSIS_TASK, 
NEW_TASK_TEMPLATE_ANALYSIS_TASK: NewTaskTemplateAnalysis_,

# singlePageNavigation.js
var NewTaskTemplateAnalysis = "NewTaskTemplateAnalysis";
urlMappings["/" + NewTaskTemplateAnalysis + "/"] = NewTaskTemplateAnalysis;

# urls.py
from NewTaskTemplateAnalysis import urls as NewTaskTemplateAnalysis_urls
url(r'^NewTaskTemplateAnalysis/', include(NewTaskTemplateAnalysis_urls.urlpatterns)),
```