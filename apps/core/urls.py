from django.conf.urls.defaults import patterns, url
from core.views import AccountView

urlpatterns = patterns('',
    #url(r'^read/(?P<user_id>.+)/$', AccountView.as_view(), name='account_get'),
    url(r'^read/$', AccountView.as_view(), name='account_get'),
)
