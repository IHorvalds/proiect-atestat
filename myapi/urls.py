from django.conf.urls import url
from myapi.views import ContentViewSet, UserViewSet, api_root, frontpage, blog, about_us, pictures
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


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
}, renderer_classes=[renderers.TemplateHTMLRenderer, renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

#urls
urlpatterns = [
    #Almost static stuff
    url(r'^$', frontpage, name='index'),
    url(r'^blog/$', blog, name='blog'),
    url(r'^about-us/$', about_us, name='about us'),
    url(r'^pictures/$', pictures, name='pictures'),
    #API Endpoints
    url(r'^api/$',
        api_root,
        name='api-root'),
    url(r'^api/content/$',
     content_list,
     name='content-list'),
    url(r'^api/content/(?P<pk>[0-9]+)/$',
     content_detail,
     name='content-detail'),
    url(r'^blog/(?P<pk>[0-9]+)/$',
     content_presentation,
     name='content-presentation'),
    url(r'^api/users/$',
     user_list,
     name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$',
     user_detail,
     name='user-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
