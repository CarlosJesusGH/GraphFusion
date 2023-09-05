# To create a new option with this template follow the next steps
- Copy+paste folder "WebServer/a_NewTaskTemplate" and change the name for your choice
- If it's a "Properties" type of option, remove the files: NewTaskTemplateAnalysis.py, and NewTaskTemplateResult.py. Otherwise, remove those containing "Properties" in the name.
- Change the names for the "*Analysis.py" and "*Result.py" files and their corresponding inner class, save modified files, and continue.
- Search in the new directory for the word "newtasktemplate".
- Start by opening the "settings.py" file and change every occurrence with the corresponding substitute. NOTE: The change for variables should be done using F2 in order to update all the references.
- Keep replacing other occurrences from other files.
- Search in the whole project for the word "flag:newtasktemplate" (add the following to the field to exclude files "*readme.md, *analysis.html"). This will show important places where you need to include a reference to the new option
- Copy+paste folder "WebServer/template/a_NewTaskTemplate" and change the name for your choice
- Search into the new folder for the word "newtasktemplate". change the necessary references.
- Delete the readme.md file in the new directory


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