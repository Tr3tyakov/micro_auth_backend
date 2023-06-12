from fastapi import HTTPException

from src.user.dependens.auth_guard import check_token


def extract_user_from_token(info):
    request = info.context.get('request')
    token = request.headers.get('Authorization')
    if token is not None:
        extracted_token = token.split(' ')[1]
        try:
            return check_token(extracted_token)['user']
        except HTTPException as exec:
            raise exec
