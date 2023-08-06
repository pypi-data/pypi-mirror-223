import os
from functools import wraps
from urllib.parse import urlparse

from flask import request
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

def db_session(local_session: sessionmaker, default_schema: str):
    """
    Method to be used as decorator, which accepts instance of KeycloakOpenID
    :param local_session: sessionmaker
    :return: Error message | original function
    """
    def funct_decorator(org_function):
        @wraps(org_function)
        def start_session(*args, **kwargs):
            with local_session() as session:
                subdomain = default_schema
                if len(urlparse(request.url).hostname.split('.')) > 1:
                    subdomain = f"tenant_{urlparse(request.url).hostname.split('.')[0]}"
                elif request.headers.get("X-Tenant-Id"):
                    subdomain = f"tenant_{request.headers.get('X-Tenant-Id')}"
                session.execute(text(f"SET search_path TO {subdomain}"))
                func_response = org_function(session,*args, **kwargs)
            return func_response
        return start_session

    return funct_decorator