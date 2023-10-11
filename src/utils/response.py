# Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList


def specific_object_error_response(message):
    return Response({"data": {}, "success": False, "message": message, "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST)


def get_error_strings(errors: dict):
    return_msg = ""
    for key, value in errors.items():
        for msg in value:
            if isinstance(msg, str):
                if msg == "This field is required.":
                    msg = msg.replace("This", key)
                return_msg += f"{msg}\n"
            elif isinstance(msg, dict):
                return_msg += get_error_strings(msg)
    return return_msg.split("\n")[0]

def error_response(serializer):
    errors = serializer.errors[0] if type(serializer.errors) == ReturnList else serializer.errors
    error_msg = get_error_strings(errors)

    return Response({"data": serializer.errors, "success": False, "message": error_msg, "status_code": 400},
                    status=status.HTTP_400_BAD_REQUEST)


def error_response_account_not_verified(serializer):
    errors = serializer.errors

    message = get_error_strings(errors)
    response = {"data": errors, "success": False, "message": message, "status_code": 401, }
    if "is_verified" in errors:
        response["is_verified"] = False
        response['status_code'] = 200
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)

    return Response(response, status=status.HTTP_400_BAD_REQUEST)


def success_response(serializer, message, status_code=200, send_data=True):

    response = {'success': True, 'message': message, "status_code": status_code,
                'data': serializer.data if send_data else {}}
    if serializer.__class__.__name__ == "LoginSerializer":
        response['is_verified'] = True
    return Response(response, status=status_code)


def success_response_message(data, message, status_code=200, send_data=True):
    response = {'success': True, 'message': message, "status_code": status_code, 'data': data if send_data else {}}
    return Response(response, status=status_code)
