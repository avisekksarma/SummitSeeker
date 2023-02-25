# Utility functions/classes across the project
from rest_framework.views import exception_handler

# if success then read data,
# if success = False, then if validation_error = True, then read errors
# else if validation = False, then read message
def makeResponse(message='', isSuccess=False, data=None, validation_error=False,token_invalid=False, **kwargs):
    response = {
        "message": message,
        "success": isSuccess,
        "data": data,
        "validation_error": validation_error,
        "token_invalid":token_invalid,
        **kwargs
    }
    return response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None and response.data['code']=='token_not_valid':
        res = makeResponse('Token invalid/expired',token_invalid=True)
        response.data = res
    elif response is not None:
        response.data['success'] = False 
    # if response.data.get('')
    return response



def log(val,delim="-"):
    for i in range(30):
        print(delim,end='')
    print()
    print(val)
    for i in range(30):
        print(delim,end='')
    print()


