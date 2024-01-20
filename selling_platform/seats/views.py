from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

@api_view()
def say_hello(request):
    return Response('Hello world')
