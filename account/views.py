import json

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as l, logout as l_out

# Create your views here.
from account.models import User
from product.models import Report, Product


def signin(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return JsonResponse({"message": "user not found"}, status=404)

    else:
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return JsonResponse({"message": "ok"}, status=200)


def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        l(request, user)
        return JsonResponse({"message": "ok"}, status=200)
    else:
        return JsonResponse({"message": "user not found"}, status=404)


def logout(request):
    l_out(request)
    return JsonResponse({"message": "ok"}, status=200)


def create_report(request):
    user = request.user

    if not request.user.is_authenticated:
        return JsonResponse({"message": "unauthorized"}, status=401)
    data = json.loads(request.body)
    product = data.get('product')
    if not product or not Product.objects.get(id=product):
        return JsonResponse({"message": "unauthorized"}, status=404)
    detail = product.data.get('detail')
    reason = "spam content" if product.data.get('reason') == 1 else "inappropriate content"
    Report.objects.create(user=user, product=Product.objects.get(id=product))
