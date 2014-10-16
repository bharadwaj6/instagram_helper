from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instagram_helper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'best_time_teller.views.index', name='index'),
    url(r'^home\w*/$', 'best_time_teller.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
