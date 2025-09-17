from rest_framework.response import Response

def custom_response(message, data=None, status_code=200):
    return Response({
        "status_code": status_code,
        "message": message,
        "data": data
    }, status=status_code)
