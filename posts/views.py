from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import generics, permissions, filters
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    Enables viewing of posts, and creation of posts only by logged-in users.
    Posts display counts of likes and comments and are ordered by creation date,
    newest first. Enables filtering of posts by profiles and searching by title
    or username, as well as sorting by likes count, comments count and most
    recently liked. New posts are assigned to the currently authenticated user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Enables detailed viewing of a post, and updating and deletion of a post
    only by its owner. Posts display counts of likes and comments and are
    ordered by creation date, newest first.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
