# Utility functions/classes across the project
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['success'] = False
    return response



def log(val,delim="-"):
    for i in range(30):
        print(delim,end='')
    print()
    print(val)
    for i in range(30):
        print(delim,end='')
    print()
