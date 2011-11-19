from django.conf.urls.defaults import patterns, url
from core.views import ExtJsInstanceModelView

from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ListModelView
from core.resources import AccountResource


urlpatterns = patterns('',
    #url(r'^read/(?P<user_id>.+)/$', AccountView.as_view(), name='account_get'),
    #url(r'^read/$', AccountView.as_view(), name='account_get'),
    url(r'^read/(?P<owner>[^/]+)/$', ListModelView.as_view(resource=AccountResource), name='accounts-list'),
    url(r'^read/(?P<owner>[^/]+)/(?P<id>[^/]+)/$', ExtJsInstanceModelView.as_view(resource=AccountResource), name='accounts-read'),
)
