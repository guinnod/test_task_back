from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['text', 'likes', 'title', 'pk']

    def get_likes(self, obj):
        return len(obj.liked_users.all())

    def get_title(self, obj):
        return User.objects.get(pk=obj.user.pk).email