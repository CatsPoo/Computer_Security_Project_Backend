# from django.http import HttpResponseServerError

# class ExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#         except Exception as e:
#             response = HttpResponseServerError("Oops! Something went wrong.")
#         return response