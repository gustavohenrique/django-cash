from djangorestframework import status, permissions
from djangorestframework.response import ErrorResponse
from djangorestframework.views import InstanceModelView, ListOrCreateModelView
from django.http import QueryDict


DEFAULT_ERROR_RESPONSE = ErrorResponse(status.HTTP_404_NOT_FOUND, {'total':'0', 'data':[], 'success':'false'})

class ExtJsInstanceModelView(InstanceModelView):
    permissions = (permissions.IsAdminUser,)
    
    def get(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).get(request, *args, **kwargs)
        except:
            raise DEFAULT_ERROR_RESPONSE 


class ExtJsCreateModelView(ListOrCreateModelView):
    permissions = (permissions.IsAdminUser,)

    def initial(self, request, *args, **kwargs):
        params_str = request.POST.values()[0]
        formatted_str = params_str.replace("'","").replace(": ","=").replace(", ","&").replace("{","").replace("}","")
        formatted_str = formatted_str + ('&user=%s' % request.user.id)
        request.POST = QueryDict(formatted_str)
        self.request = request

    def post(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).post(self.request, *args, **kwargs)
        except:
            raise DEFAULT_ERROR_RESPONSE 


class ExtJsUpdateModelView(InstanceModelView):
    permissions = (permissions.IsAdminUser,)

    def initial(self, request, *args, **kwargs):
        raw_data = request.raw_post_data
        import ipdb; ipdb.set_trace()
        raw_data = raw_data.split('[')[1].replace(']}','')
        request.raw_post_data = raw_data
        self.request = request

        formatted_str = raw_data.replace("'","").replace(": ","=").replace(", ","&").replace("{","").replace("}","")
        formatted_str = formatted_str + ('&user=%s' % request.user.id)
        self._content = QueryDict(formatted_str)

    def put(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).put(self.request, *args, **kwargs)
        except:
            raise DEFAULT_ERROR_RESPONSE
 
