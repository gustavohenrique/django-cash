from djangorestframework import status, permissions
from djangorestframework.response import ErrorResponse
from djangorestframework.views import InstanceModelView


class ExtJsInstanceModelView(InstanceModelView):
    permissions = (permissions.IsAdminUser, )
    
    def get(self, request, *args, **kwargs):
        try:
            return super(self.__class__, self).get(request, *args, **kwargs)
        except:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, {'total':'0', 'data':[], 'success':'false'})

