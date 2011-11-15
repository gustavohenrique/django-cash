from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status

class AccountView(View):

    def get(self, request):
        return '%s' % request

