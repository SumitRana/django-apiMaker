from django.core.management.base import BaseCommand, CommandError
import os
from ApiMaker.helper import *

class Command(BaseCommand):
    help = 'Command to do........'

    code_string = '''from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json

class {0}HttpInterface(View):

    @method_decorator(attribute_access_blocker(['meal_time'],'get'))
    def get(self,request):
        result = dict()
        status = 200
        try:
            post_data = json.loads(request.GET['q'])
            print post_data
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
            for diet in post_data['data']:
                p = {0}(**diet)
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
            with open(os.getcwd()+"/"+str(options['appname'])+"/"+str(options['model'])+"HttpInterface.py","w") as f:
                f.write(self.code_string.format(str(options['model'])))
            print("Command Successful")
        except Exception as e:
            print(str(e))
            CommandError(repr(e))