from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^url$', 'onlineviewer.views.viewurltests'),
    url(r'^proxy$', 'onlineviewer.views.viewproxystatus'),
    url(r'^dns$', 'onlineviewer.views.viewdnstests'),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
)
