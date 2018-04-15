from django.conf.urls import url
from myapi.views import ContentViewSet, UserViewSet, api_root
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


content_list = ContentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

content_detail = ContentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'detele': 'destroy'
})

content_presentation = ContentViewSet.as_view({
    'get': 'present'
}, renderer_classes=[renderers.TemplateHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

#API Endpoints
urlpatterns = [
    url(r'^$', api_root),
    url(r'^content/$',
     content_list,
     name='content-list'),
    url(r'^content/(?P<pk>[0-9]+)/$',
     content_detail,
     name='content-detail'),
    url(r'^content/(?P<pk>[0-9]+)/presentation/$',
     content_presentation,
     name='content-presentation'),
    url(r'^users/$',
     user_list,
     name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
     user_detail,
     name='user-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
