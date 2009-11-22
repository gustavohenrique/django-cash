# -*- coding: utf-8 *-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),

    (r'^auth/login/','django.contrib.auth.views.login'),
    url(r'^auth/logout/','django.contrib.auth.views.logout_then_login', name='logout'),

    (r'^$', 'money.views.index'),
    (r'^money/', include('money.urls')),
)


"""
Se o modo debug está ligado, significa que está em ambiente de desenvolvimento,
entao o django passa a servir arquivos estáticos.
"""
if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    )
