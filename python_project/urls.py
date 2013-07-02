from django.conf.urls import patterns, include, url
from django.conf import settings
from my_calendar.views import homepage, LoginView, SignupView
#import my_calendar.views
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', homepage, name='homepage'),
#    # url(r'^admin/', include(admin.site.urls)),
#     # url(r'^my_calendar/', include('my_calendar.urls'))
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^registration/$', SignupView.as_view(), name='registration'),
#     # url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
