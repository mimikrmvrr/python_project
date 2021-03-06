from django.conf.urls import patterns, include, url
from django.conf import settings
from my_calendar.views import homepage,
                              LoginView,
                              SignupView,
                              CreateEventView,
                              eventslist,
                              eventpage,
                              logout_view,
                              groups,
                              CreateGroupView,
                              PostCommentView


urlpatterns = patterns('',
    url(r'^$', homepage, name='homepage'),
#    # url(r'^admin/', include(admin.site.urls)),
#     # url(r'^my_calendar/', include('my_calendar.urls'))
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^registration/$', SignupView.as_view(), name='registration'),
    url(r'^error_registration/$',
        SignupView.as_view(),
        name='error_registration'),
    url(r'^create_event/$', CreateEventView.as_view(), name='create_event'),
    url(r'^error_event/$', CreateEventView.as_view(), name='error_event'),
    url(r'^events/(?P<id>\d+)/$', eventpage, name='event'),
    url(r'^events/$', eventslist, name='eventslist'),
    url(r'^groups/$', groups, name='groupslist'),
    url(r'^create_group/$', CreateGroupView.as_view(), name='create_group'),
    url(r'^error_group/$', CreateGroupView.as_view(), name='error_group'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
