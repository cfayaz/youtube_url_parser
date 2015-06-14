from django.conf.urls import include, url
from youtubeRESTapp.views import MyRESTView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^parse/(?P<video_id>\w+)/$', MyRESTView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])