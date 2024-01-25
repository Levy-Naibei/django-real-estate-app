from rest_framework.exceptions import APIException


class PropertyNotFound(APIException):
    status_code = 404
    details = "Property requested does not exist."
