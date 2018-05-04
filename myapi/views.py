# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from myapi.models import Content
from myapi.serializers import ContentSerializer
from django.contrib.auth.models import User
from myapi.serializers import UserSerializer
from rest_framework import permissions, viewsets, renderers, generics, mixins, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, detail_route, permission_classes, renderer_classes
from rest_framework.reverse import reverse
from myapi.permissions import IsOwnerOrReadOnly
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import File
import os, os.path
import mammoth
import codecs

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None): # Entry point for the API
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'content': reverse('content-list', request=request, format=format)
    })

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
     # TODO: add templates for all content types

    ##IDEA: for single server implementation: use different ports for the api(port: plain 4279, secure 4280) and the user-facing website(port: plain 80, secure 443)

    @detail_route(renderer_classes=[TemplateHTMLRenderer, JSONRenderer, StaticHTMLRenderer,], methods=['GET', ])
    def present(self, request, *args, **kwargs):
        content = self.get_object()
        if content.filetype in ['jpg', 'jpeg', 'png']:
            imageHeight = self.request.query_params.get('height', None)
            imageWidth = self.request.query_params.get('width', None)
            return Response({'content': content, 'height': imageHeight, 'width': imageWidth}, template_name = 'myapi/image_piece.html')
        elif content.filetype == 'html':
            return Response({'content': content}, template_name = 'myapi/BlogPost.html')
        else:
            return HttpResponse(content.actualfile) #if we don't know what it is, then just show it


    def perform_create(self, serializer):
        if self.request.data['author']:
            serializer.save(owner=self.request.user)
        else:
            serializer.save(owner=self.request.user, author=self.request.user)

    def update(self, request, *args, **kwargs):
        content = self.get_object()
        content.title = str(request.data['title'])
        content.subtitle = str(request.data['subtitle'])
        content.author = str(request.data['author'])
        content.description = str(request.data['description'])
        if 'ispublic' in request.data:
            content.ispublic = request.data['ispublic'][0].lower()
        else:
            content.ispublic = 'f'
        #Replace content.actualfile
        filepath = content.actualfile.path
        if request.data['actualfile']:
            fh = open(filepath, "rwb")
            content.actualfile.save(os.path.basename(content.actualfile.path), localConvertDocxToHtml(request.data['actualfile'], content.actualfile, request.data['actualfile'].name), save=True)
            try:
                os.remove(filepath)
            except:
                print("Coulnd't remove " + filepath)
        else:
            content.actualfile.save(os.path.basename(content.actualfile.path), File(open(content.actualfile.path, "rb")), save=True)
        content.filetype = content.getFileType()
        #Replace content.articleimage - WORKING
        imagepath = content.articleimage.path
        if request.data['articleimage']:
            image = request.data['articleimage']
            content.articleimage.save(os.path.basename(imagepath), image, save=True)
            try:
                os.remove(imagepath)
            except:
                print("Couldn't delete " + imagepath)
        else:
            content.articleimage.save(os.path.basename(imagepath), File(open(imagepath, "rb")), save=True)
        return Response(content)

    def delete(self, request, **kwargs):
        content = self.get_object()
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def localConvertDocxToHtml(content, contentToUpdate, path):
    print(path.split('.')[-1])
    if path.split('.')[-1] == 'docx':
        result = mammoth.convert_to_html(content.file)
        fh1 = open(contentToUpdate.path, "wb")
        print(contentToUpdate.path)
        fh1.write(result.value.encode('utf-8')) #we're writing at the resource(i.e. path) we're going to be copying to the self.actualfile
        fh1.close()
        return File(open(contentToUpdate.path, "rb"))
    elif path.split('.')[-1] == 'html':
        return content.file

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def frontpage(request):
    content = Content.objects.filter(ispublic=True, filetype='html').order_by('-id')[:1]
    #html = codecs.open(content[0].actualfile.path, "r", "utf-8")
    #return Response({'content': content[0], 'contentHTML': html.read()}, template_name='myapi/Home.html')
    return Response({'content': content}, template_name='myapi/Home.html')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def blog(request):
    queryset = Content.objects.filter(ispublic=True, filetype='html').order_by('-id')
    return Response({'articles': queryset}, template_name='myapi/Blog.html')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def pictures(request):
    queryset = Content.objects.filter(ispublic=True, filetype__in=['png', 'jpg', 'jpeg']).order_by('-id')
    return Response({'pictures': queryset}, template_name='myapi/Pictures.html')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def about_us(request):
    return Response(template_name='myapi/AboutUs.html')
