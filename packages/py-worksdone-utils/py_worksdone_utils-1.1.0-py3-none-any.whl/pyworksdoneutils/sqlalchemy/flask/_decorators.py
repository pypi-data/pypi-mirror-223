import logging
import os
from functools import wraps
from typing import Optional, Callable
from urllib.parse import urlparse

from flask import request
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

def db_session(local_session: sessionmaker, tenant_extractor: Optional[Callable[[], str]] = lambda: "",):
    """
    Method to be used as decorator, which accepts instance of KeycloakOpenID
    :param local_session: sessionmaker
    :return: Error message | original function
    """
    def funct_decorator(org_function):
        @wraps(org_function)
        def start_session(*args, **kwargs):
            with local_session() as session:
                subdomain = f"tenant_{tenant_extractor()}"
                logging.info(f"Database session tenant: {subdomain}")
                session.execute(text(f"SET search_path TO {subdomain}"))
                func_response = org_function(session,*args, **kwargs)
            return func_response
        return start_session

    return funct_decorator