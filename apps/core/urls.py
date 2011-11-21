from django.conf.urls.defaults import patterns, url
from core.views import ExtJsInstanceModelView, ExtJsCreateModelView, ExtJsUpdateModelView

from djangorestframework.views import ListModelView
from core.resources import AccountResource


urlpatterns = patterns('',
    url(r'^list/(?P<user>[^/]+)/$', ListModelView.as_view(resource=AccountResource), name='accounts-list'),
    url(r'^read/(?P<id>[^/]+)/$', ExtJsInstanceModelView.as_view(resource=AccountResource), name='accounts-read'),
    url(r'^create/$', ExtJsCreateModelView.as_view(resource=AccountResource), name='accounts-create'),
    url(r'^update/(?P<id>[^/]+)/$', ExtJsUpdateModelView.as_view(resource=AccountResource), name='accounts-update'),
)
