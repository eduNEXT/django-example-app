from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


urlpatterns = patterns(
    '',
    # Tech
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name="robots.txt"),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain'), name="humans.txt"),
    url(r'^$', TemplateView.as_view(template_name='main.html'), name="main"),

    # Django apps

    # Admin panel and documentation:
    url(r'^admin/', include(admin.site.urls)),
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
