from .models import Task
from django.contrib import admin


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'taskName', 'user', 'taskId', 'finished', 'task_type', 'started_at', 'finished_at', 'operational_directory',
        "error_text", 'error_occurred',)
    list_editable = ('finished', 'task_type', 'error_occurred',)
    ordering = ('taskId',)

