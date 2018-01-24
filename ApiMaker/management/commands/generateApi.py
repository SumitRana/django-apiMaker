from django.core.management.base import BaseCommand, CommandError
import os
from ApiMaker.helper import *

class Command(BaseCommand):
    help = 'Command to do........'

    template_for_string_based_models = '''from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import {0}
from django.views import View
import json

class {0}HttpInterface(View):

    def get(self,request):
        result = dict()
        status = 200
        try:
            post_data = request.GET
            diets = {0}.objects.filter(**post_data)
            result['result'] = "SUCCESS"
            result['data'] = [ Serialize.serializeDjangoModel(diet) for diet in diets]
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response

    def post(self,request):
        result = dict()
        status = 200
        try:
            post_data = json.loads(request.body)
            for instanceDict in post_data['data']:
                p = {0}(**instanceDict)
                p.save()
            result['result'] = "SUCCESS"
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response

    def delete(self,request):
        result = dict()
        status = 200
        try:
            post_data = json.loads(request.body)
            {0}.objects.get(pk=post_data['id']).delete()
            result['result'] = "SUCCESS"
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response'''

    template_for_file_based_models = '''from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

class PostHttpInterface(View):

    def get(self,request):
        result = dict()
        status = 200
        try:
            post_data = request.GET
            diets = Post.objects.filter(**post_data)
            result['result'] = "SUCCESS"
            result['data'] = [ Serialize.serializeDjangoModel(diet) for diet in diets]
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response

    def post(self,request):
        result = dict()
        status = 200
        try:
            post_data = request.POST
            args = dict()
            for pkey in request.POST.keys():
                args[str(pkey)] = request.POST[pkey]
            for fkey in request.FILES.keys():
                args[str(fkey)] = request.FILES[fkey]
            
            p = Post(**args)
            p.save()
            result['result'] = "SUCCESS"
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response

    def delete(self,request):
        result = dict()
        status = 200
        try:
            post_data = json.loads(request.body)
            Post.objects.get(pk=post_data['id']).delete()
            result['result'] = "SUCCESS"
        except Exception as e:
            result['result'] = "FAILURE"
            result['error_reason'] = str(e)
            status = 500
        response = JsonResponse(result,status=status)
        response['status'] = status
        return response'''

 
    def add_arguments(self, parser):
        parser.add_argument('appname', type=str)
        parser.add_argument('model',type=str)
        
    def handle(self, *args, **options):
        try:
            # your logic here
            print(options)
            contains_file_storage = False
            
            with open(os.getcwd()+"/"+str(options['appname'])+"/"+str(options['model'])+"HttpInterface.py","w") as f:
                f.write(self.code_string.format(str(options['model'])))
            print("Command Successful")
        except Exception as e:
            print(str(e))
            CommandError(repr(e))