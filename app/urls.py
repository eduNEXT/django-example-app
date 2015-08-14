from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from app.djangoapps.counter.views import VisitorCounter, UserActivityEndPoint, HeartBeat
# from rest_framework.routers import DefaultRouter

#admin.autodiscover()

# router = DefaultRouter()
# router.register(r'activity', UserActivityViewSet)


urlpatterns = patterns('',

                       # Tech
                       url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name="robots.txt"),
                       url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain'), name="humans.txt"),
                       url(r'^favicon\.ico$', RedirectView.as_view(url=(settings.STATIC_URL + 'ico/favicon.ico')), name="favicon.ico"),
                       # url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),

                       # Django apps
                       url(r'^counter/(?P<path>.*)$', VisitorCounter.as_view(), name='counter_endpoint'),
                       url(r'^usercount/$', UserActivityEndPoint.as_view(), name='counter_printpoint'),
                       url(r'^heartbeat/$', HeartBeat.as_view(), name='heartbeat'),

                       # Admin panel and documentation:
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^', include(router.urls)),
                       )

urlpatterns += staticfiles_urlpatterns()


# TODO: Check if we really need this with the dev/prod configuration
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'', include('django.contrib.staticfiles.urls')),
                           url(r'^__debug__/', include(debug_toolbar.urls)),
                           ) + urlpatterns
