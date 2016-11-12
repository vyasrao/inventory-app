from django.shortcuts import render_to_response
from inventory.BusinessLayer import NotifyLayer, UsersLayer


def notifications(request, user_id):

    context = {"user_id" : user_id}
    context["all_notifications"] = NotifyLayer.show_notification(user_id, True)
    context["username"] = UsersLayer.get_username(user_id)

    return render_to_response('notification.html', context)


def clear_notify(request, user_id):

    context = {"user_id" : user_id}
    context["all_notifications"] = NotifyLayer.clear_notification(user_id)
    context["username"] = UsersLayer.get_username(user_id)

    return render_to_response('notification.html', context)
