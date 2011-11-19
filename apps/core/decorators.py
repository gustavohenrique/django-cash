# -*- coding: utf-8 -*-
from djangorestframework.authentication import UserLoggedInAuthentication
from djangorestframework.response import Response


def login_required(method_to_decorate):
    def authenticate(self, request):
        auth = UserLoggedInAuthentication(self)
        user = auth.authenticate(request)
        if user is None:
            return Response(status.HTTP_403_NOT_FOUND)
        return method_to_decorate(self, request)
    return authenticate
