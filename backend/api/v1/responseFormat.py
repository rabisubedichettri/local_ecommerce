from rest_framework.response import Response
import json


def responseFormat(status="", message="", data=[], errors=[],):
    format = {
        "message": message,
        "data": data,
        "errors": errors,
    }
    return Response(data=format,content_type="application/json",status=status)