from django.conf.urls.defaults import patterns, url
from core.views import AccountView

urlpatterns = patterns('',
    url(r'^$', AccountView.as_view(), name='account'),
)
