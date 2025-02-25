from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, \
    FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class FollowViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Follow.objects.filter(user=request.user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FollowSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
