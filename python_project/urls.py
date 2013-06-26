from django.conf.urls import patterns, include, url
from django.conf import settings
# from my_calendar.views import homepage
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
#     url(r'^$', homepage, name='homepage'),
#    # url(r'^admin/', include(admin.site.urls)),
#     # url(r'^my_calendar/', include('my_calendar.urls'))
#     # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
#     # url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#         (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )

