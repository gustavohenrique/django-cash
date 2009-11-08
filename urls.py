from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^auth/login/','django.contrib.auth.views.login'),
    (r'^auth/logout/','django.contrib.auth.views.logout_then_login'),

    (r'^$', 'money.views.index'),
    (r'^money/', include('money.urls')),
)

from django.conf import settings
urlpatterns += patterns('',
  (r'^media/(.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
