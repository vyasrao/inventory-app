import time
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from inventory.BusinessLayer import ProductsLayer, VariantsLayer, NotifyLayer, UsersLayer


def variants(request, user_id, product_id):

    context = {
        "user_id": user_id,
        "product_id": product_id,
        "product_name": ProductsLayer.get_product_name(product_id)
    }

    context["username"] = UsersLayer.get_username(user_id)
    context["variants"] = VariantsLayer.get_valid_variants(product_id)
    context["notifications"] = NotifyLayer.show_notification(user_id, True)

    return render_to_response('variant.html', context)


def add_variant(request):

    response_data = {"status": False}

    if request.method == "POST":

        user_id = request.POST.get("user_id")
        product_id = request.POST.get("product_id")
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("desc")
        sell_price = request.POST.get("sell")
        cost_price = request.POST.get("cost")
        options = json.loads(request.POST.get("options"))

        status, info = VariantsLayer.insert_variant(product_id, name, code, description, user_id, sell_price, cost_price, options)

        response_data["status"] = status
        response_data["info"] = info
    else:
        response_data["info"] = "Some serious problem!"

    return HttpResponse(json.dumps(response_data),content_type="application/json")


def edit_variant(request):

    response_data = {"status": False}

    if request.method == "POST":

        user_id = request.POST.get("user_id")
        product_id = request.POST.get("product_id")
        variant_id = request.POST.get("id")
        date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

        values = {
            "user_id": user_id,
            "date_stamp": date_stamp
        }

        notifications = []

        if not request.POST.get("name") is None:
            variant_name = request.POST.get("name")

            if not VariantsLayer.is_unique_variant_name_e(product_id, variant_id, variant_name):
                response_data["info"] = "Variant name must be unique"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            values["name"] = variant_name
            notifications.append(4)

        if not request.POST.get("code") is None:
            variant_code = request.POST.get("code")

            if not VariantsLayer.is_unique_variant_code_e(product_id, variant_id, variant_code):
                response_data["info"] = "Variant code must be unique"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            values["code"] = request.POST.get("code")
            notifications.append(5)

        if not request.POST.get("desc") is None:
            values["description"] = request.POST.get("desc")
            notifications.append(6)

        if not request.POST.get("sell") is None:
            values["selling_price"] = request.POST.get("sell")
            notifications.append(7)

        if not request.POST.get("cost") is None:
            values["cost_price"] = request.POST.get("cost")
            notifications.append(8)

        if not request.POST.get("options") is None:
            values["options"] = json.loads(request.POST.get("options"))

        status, info = VariantsLayer.update_variant(variant_id, user_id, values, notifications, date_stamp)

        response_data["status"] = True
        response_data["info"] = "Success!!"

    else:
        response_data["info"] = "Some serious problem! You must demand for refund!!"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_variant(request):

    response_data = {"status": False}

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        user_id = request.POST.get("user_id")
        variant_id = request.POST.get("variant_id")

        status, info = VariantsLayer.delete_variant(variant_id, user_id)

        response_data["status"] = status
        response_data["info"] = info

    else:
        response_data["info"] = "Some serious problem! You must demand for refund!!"

    return HttpResponse(json.dumps(response_data), content_type="application/json")

