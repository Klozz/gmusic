from django.conf.urls import *
from downloader.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^json/search/$', buscar_cancion_json, name='buscar_cancion_json'),
    url(r'^admin/', include(admin.site.urls)),
)
