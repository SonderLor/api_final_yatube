from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group


class GroupSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ("id", "title", "slug", "description")
        model = Group
        read_only_fields = ("id",)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ("id", "author", "text", "pub_date", "image", "group")
        model = Post
        read_only_fields = ("id", "author", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ("id", "author", "text", "created", "post")
        model = Comment
        read_only_fields = ("id", "author", "created", "post")
