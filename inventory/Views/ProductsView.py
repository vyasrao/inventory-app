import time
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from inventory.BusinessLayer import ProductsLayer, NotifyLayer, UsersLayer


def products(request, user_id):

    context = {"user_id": user_id}
    context["products"] = ProductsLayer.get_valid_products()
    context["notifications"] = NotifyLayer.show_notification(user_id, False)
    context["username"] = UsersLayer.get_username(user_id)

    return render_to_response('product.html', context)


def add_product(request):
    response_data = {"status": False, "info": "Some serious problem!"}

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        product_name = request.POST.get("name")
        product_code = request.POST.get("code")
        product_desc = request.POST.get("desc")

        # insert product
        status, info = ProductsLayer.insert_product(product_name, product_code, product_desc, user_id)

        response_data["status"] = status
        response_data["info"] = info

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def edit_product(request):

    response_data = {"status": False}

    if request.method == "POST":

        user_id = request.POST.get("user_id")
        product_id = request.POST.get("id")
        date_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

        values = {
            "user_id": user_id,
            "date_stamp": date_stamp
        }
        notifications = []

        if not request.POST.get("name") is None:
            product_name = request.POST.get("name")

            if not ProductsLayer.is_unique_product_name_e(product_id, product_name):
                response_data["info"] = "Product name must be unique"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            values["name"] = product_name
            notifications.append(1)

        if not request.POST.get("code") is None:
            product_code = request.POST.get("code")

            if not ProductsLayer.is_unique_product_code_e(product_id, product_code):
                response_data["info"] = "Product name must be unique"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            values["code"] = request.POST.get("code")
            notifications.append(2)

        if not request.POST.get("desc") is None:
            values["description"] = request.POST.get("desc")
            notifications.append(3)

        # update product
        status, info = ProductsLayer.update_product(product_id, user_id, values, notifications, date_stamp)

        response_data["status"] = status
        response_data["info"] = info

    else:
        response_data["info"] = "Some serious problem! You must demand for refund!!"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_product(request):

    response_data = {"status": False}

    if request.method == "POST":
        id = request.POST.get("product_id")
        user_id = request.POST.get("user_id")

        status, info = ProductsLayer.delete_product(id, user_id)

        response_data["status"] = status
        response_data["info"] = info

    else:
        response_data["info"] = "Some serious problem! You must demand for refund!!"

    return HttpResponse(json.dumps(response_data), content_type="application/json")
