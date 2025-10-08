from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_repr', 'unread', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target_repr', 'timestamp']

    def get_actor(self, obj):
        return {'id': obj.actor.id, 'username': obj.actor.username}

    def get_target_repr(self, obj):
        # return a simple representation of the target (e.g., post title or username)
        t = obj.target
        if t is None:
            return None
        # Post
        from posts.models import Post
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if isinstance(t, Post):
            return {'type': 'post', 'id': t.id, 'title': t.title}
        if isinstance(t, User):
            return {'type': 'user', 'id': t.id, 'username': t.username}
        return {'type': str(obj.target_content_type), 'id': str(obj.target_object_id)}