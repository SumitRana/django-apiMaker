import json
from django.http import JsonResponse

# for bottom-up serialization of models
class Serialize:
	@classmethod
	def serializeDjangoModel(cls,row_object):
		try:
			lcs = row_object._meta.local_fields
			local_column_names = []
			jdata = dict()
			for lc in lcs:
				value = getattr(row_object,str(lc.name))
				jdata[str(lc.name)] = cls.serializeDjangoModel(value)
			return jdata
		except Exception:
			return str(row_object)

# Access manipulator
def attribute_access(allow=None,block=None,request_type="get"):
	def outer(func):
		def wrapper(request):
			print "in access blocker"
			print list_of_attributes
			result = dict()
			try:
				if request_type is "get":
					post_data = json.loads(request.GET['q'])
				elif request_type is "post":
					post_data = json.loads(request.body)
				elif request_type is "delete":
					post_data = json.loads(request.body)

				if allow is None and block is None:
					raise Exception("server Error : allow and block both cannot be None")

				if block is not None:
					# access block
					unallowed_fields = list(set(list(post_data)).intersection(set(list(list_of_attributes))))
				else:
					# access provide
					unallowed_fields = list(set(list(post_data)).difference(set(list(list_of_attributes))))

				print(unallowed_fields)
				if len(unallowed_fields) is not 0:
					status = 403
					result['result'] = str(unallowed_fields)+" : are private to server."
					response = JsonResponse(result,status=status)
					response['status'] = status
					return response
			except Exception as e:
				status = 500
				result['result'] = str(e)
				response = JsonResponse(result,status=status)
				response['status'] = status
				return response
			return func(request)
		return wrapper
	return outer