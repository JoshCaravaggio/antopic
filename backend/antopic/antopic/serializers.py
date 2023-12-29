from rest_framework import serializers
from .models import Topic, Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['_id', 'filename', 'type', 'url', 'title', 'state']

class TopicSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, write_only=True)
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['_id', 'user_id', 'title', 'description', 'contents']