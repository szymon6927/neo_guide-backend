from rest_framework.exceptions import APIException


class BusinessLogicAPIException(APIException):
    status_code = 422
    default_detail = 'Business rules were broken.'
    default_code = 'business_logic_error'
