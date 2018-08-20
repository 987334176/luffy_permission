from django.shortcuts import render, redirect,HttpResponse

def login(request):
    return render(request,"login.html")

