from django.shortcuts import render_to_response
from inventory.BusinessLayer import UsersLayer


def index(request):

    context = {"users": UsersLayer.get_valid_users()}

    return render_to_response('index.html', context)


