from rest_framework import serializers
from myapi.models import Content
from django.contrib.auth.models import User

class ContentSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    presentation = serializers.HyperlinkedIdentityField(view_name='content-presentation')
    path = serializers.ReadOnlyField()
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True, allow_blank=False, max_length=50)
    # path = serializers.CharField(required=True, allow_blank=False)
    # description = serializers.CharField()
    # owner = serializers.ReadOnlyField(source='owner.username')
    # filetype = serializers.CharField()

    class Meta:
        model = Content
        fields = ('url', 'id', 'presentation', 'path', 'owner', 'title', 'actualfile', 'description', 'owner', 'filetype')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    content_files = serializers.HyperlinkedRelatedField(many=True, view_name='content-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'content_files')
