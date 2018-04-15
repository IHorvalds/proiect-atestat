# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from myapi.models import Content
from myapi.serializers import ContentSerializer
from django.contrib.auth.models import User
from myapi.serializers import UserSerializer
from rest_framework import permissions, viewsets, renderers, generics, mixins
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, detail_route
from rest_framework.reverse import reverse
from myapi import permissions as permi

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          permi.IsOwnerOrReadOnly)
    template_name = 'myapi/image_piece.html' #TODO: add templates for all content types

    ##IDEA: for single server implementation: use different ports for the api(port: plain 4279, secure 4280) and the user-facing website(port: plain 80, secure 443)

    @detail_route(renderer_classes=[TemplateHTMLRenderer, ])
    def present(self, request, *args, **kwargs):
        content = self.get_object()
        return Response({'content': content})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class ContentList(generics.ListCreateAPIView): #  List all content file entries or create a new entry
#     queryset = Content.objects.all()
#     serializer_class = ContentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, permi.IsOwnerOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class ContentDetail(generics.RetrieveUpdateDestroyAPIView): # Retrieve/update/delete a content file entry
#     #queryset = Content = Content.objects.all()
#     queryset = Content.objects.all()
#     serializer_class = ContentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, permi.IsOwnerOrReadOnly)
#
# class ContentPresentation(generics.GenericAPIView):
#     queryset = Content.objects.all()
#     renderer_classes = [TemplateHTMLRenderer, ]
#     template_name = 'myapi/image_piece.html'
#
#     def get(self, request, *args, **kwargs): #TODO: Return a response as either an image, sound clip, video clip, formatted text (html) or file page
#         content = self.get_object()
#         # content_types = {
#         # 'jpg':  Response(content, template_name='image_piece.html')# IMAGES ##TODO: Not sure if this works?
#         # 'jpeg': Response(content, template_name='image_piece.html')
#         # 'png':  Response(content, template_name='image_piece.html')
#         # 'rtf':  Response(content, template_name='text_piece.html')# FORMATTED TEXT
#         # 'html': Response(content, template_name='text_piece.html')
#         # 'pdf':  Response(content, template_name='pdf_piece.html')# Errmm?
#         # 'mp3':  Response(content, template_name='audio_piece.html')# SOUND
#         # 'wav':  Response(content, template_name='audio_piece.html')
#         # 'zip':  Response(content, template_name='misc_piece.html')# MISCELLANEOUS FILES
#         # '7zip': Response(content, template_name='misc_piece.html')
#         # 'rar':  Response(content, template_name='misc_piece.html')
#         # 'mp4':  Response(content, template_name='video_piece.html')# VIDEO
#         # }
#         return Response({'content': content})

###################################################################################################################################################################

# class ContentList(APIView):
#     #  List all content file entries or create a new entry
#
#     def get(self, request, format=None):
#         content_files = Content.objects.all()
#         serializer = ContentSerializer(content_files, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ContentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ContentDetail(APIView):
#     # Retrieve/update/delete a content file entry
#
#     def get_object(self, pk):
#         try:
#             return Content.objects.get(pk=pk)
#         except Content.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         content_file = self.get_object(pk)
#         serializer = ContentSerializer(content_file)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         content_file = self.get_object(pk)
#         serializer = ContentSerializer(content_file, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         content_file = self.get_object(pk)
#         content_file.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
