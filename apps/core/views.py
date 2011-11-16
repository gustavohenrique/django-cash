from djangorestframework.views import View
from djangorestframework.authentication import UserLoggedInAuthentication
from djangorestframework.response import Response
from djangorestframework import status

def login_required(request):
    auth = UserLoggedInAuthentication()
    auth.authenticate(request)

class AccountView(View):

    def get(self, request):
        auth = UserLoggedInAuthentication(self)
        user = auth.authenticate(request)
        if user is None:
            return Response(status.HTTP_403_NOT_FOUND) 

        return 'ddsfsdfs'

