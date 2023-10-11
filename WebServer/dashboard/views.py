__author__ = 'varun & carlos garcia-hernandez'

import os
from django.template.loader import get_template
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.template import Context
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from utils.UserUtils import get_name
from TaskFactory.views import get_task_view_objects_for_user
from authentication.home_page_queries import get_all_sample_networks
import unicodedata
import json

@login_required
def user_home_page(request):
    context = Context({'name': get_name(request),
                       'is_staff': request.user.is_staff,
                       'is_beta_tester': request.user.groups.filter(name='BetaTesters').exists(),
                       'networks': get_all_sample_networks(),
                       'title': 'Home'})
    context.update(csrf(request))
    return HttpResponse(get_template("dashboard/base_loggedin_home.html").render(context))

@login_required
def dashboard(request):
    result = get_task_view_objects_for_user(request=request)
    context = Context({'tasks': result})
    return HttpResponse(get_template("dashboard/results.html").render(context))

def upload_network(request):
    try:
        data = json.loads(request.POST["data"])
        data_networks = data["Networks"]
        networks = []
        # Normalize the data
        for networkData in data_networks:
            name = unicodedata.normalize('NFKD', networkData[0]).encode('ascii', 'ignore')
            network_list = unicodedata.normalize('NFKD', networkData[1]).encode('ascii', 'ignore')
            networks.append((name, network_list))
        # Check if the format is correct
        for network_name, network_data in networks:
            # print("network_name: " + network_name)
            network_data = network_data.split("\n")
            for i, line in enumerate(network_data):
                # print("line: " + line)
                # print("len(line.split())", len(line.split()), line.split())
                # print("len(line.split(','))", len(line.split(',')), line.split(','))
                # Check that the line is not empty, or not having only spaces or tabs, unless it's the last line.
                if len(line.strip()) == 0 and i != len(network_data) - 1:
                    return HttpResponseBadRequest("Error occurred while processing request: Line " + str(i+1) + " is empty")
                # Check if the line fits the format of an edge list or an adjacency matrix. If line is empty, check it's not the last one If not, return an error
                if len(line.split()) == 0 and len(line.split(',')) == 1 and i != len(network_data) - 1:
                    return HttpResponseBadRequest("Incorrect format of network. Problem in line " + str(i+1))
        # Save the networks
        for network_name, network_data in networks:
            edgelist_path = "./uploaded_networks/" + network_name
            f = open(edgelist_path, "w")
            f.write(network_data)
            f.close()
        data = json.dumps({
        'msg': "Successfully uploaded network",
        })
        return HttpResponse(data)
    except Exception as e:
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)
    
def download_networks(request):
    try:
        networks = []
        n_list = os.listdir("./uploaded_networks")
        for network_name in n_list:
            edgelist_path = "./uploaded_networks/" + network_name
            f = open(edgelist_path, "r")
            network_data = f.read()
            f.close()
            networks.append((network_name, network_data))
        data = json.dumps({
        'networks': networks,
        })
        return HttpResponse(data)
    except Exception as e:
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)
    
def delete_networks(request):
    try:
        # Delete all networks in the uploaded_networks folder
        n_list = os.listdir("./uploaded_networks")
        for network_name in n_list:
            edgelist_path = "./uploaded_networks/" + network_name
            os.remove(edgelist_path)
        data = json.dumps({
        'msg': "Successfully deleted network(s)",
        })
        return HttpResponse(data)
    except Exception as e:
        return HttpResponseBadRequest("Error occurred while processing request: " + e.message)