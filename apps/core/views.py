from djangorestframework import status, permissions
from djangorestframework.response import ErrorResponse
from djangorestframework.views import InstanceModelView, ListOrCreateModelView
from django.http import QueryDict


class ExtJsInstanceModelView(InstanceModelView, ):
    permissions = (permissions.IsAdminUser, )
    
    def get(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).get(request, *args, **kwargs)
        except:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, {'total':'0', 'data':[], 'success':'false'})


class ExtJsCreateModelView(ListOrCreateModelView):
    def initial(self, request, *args, **kwargs):
        params_str = request.POST.values()[0]
        formatted_str = params_str.replace("'","").replace(": ","=").replace(", ","&").replace("{","").replace("}","")
        request.POST = QueryDict(formatted_str)
        self.request = request

    def post(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).post(self.request, *args, **kwargs)
        except:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, {'total':'0', 'data':[], 'success':'false'})


