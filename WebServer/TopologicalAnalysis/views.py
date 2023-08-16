__author__ = 'carlos garcia-hernandez'

from types import TracebackType
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from utils.AJAX_Required import ajax_required
import logging
import json
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import unicodedata
from .settings import *
from utils.SystemCall import make_system_call
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
# task's own imports
from .TopologicalAnalysis import *

LOGGER = logging.getLogger(__name__)

@login_required
@ajax_required
def analysis_page(request):
    context = Context({
        'task_type': TOPOLOGICAL_ANALYSIS_TASK,
    })
    return HttpResponse(get_template("TopologicalAnalysis/analysis.html").render(context))
