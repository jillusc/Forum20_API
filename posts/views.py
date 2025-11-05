from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from rest_framework import generics, permissions, filters
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    Enables viewing of posts, and creation of posts only by logged-in users.
    Posts display counts of likes and comments and are ordered by creation date,
    newest first. Enables filtering of posts by profiles and searching by title,
    content and username, as well as sorting by likes count, comments count and
    most recently liked. New posts are assigned to the currently authenticated
    user. Additionally, authenticated users can mark posts as private, making them
    visible to only themselves and their followers.
    """ 
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        'content',
        'artist_name', 
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    queryset = Post.objects.all()

    def get_queryset(self):
        """
        Fetches posts for the view using the Q object which enables complex queries.
        If the user is logged-in, it gets both public posts and the user's private posts,
        plus private posts from followed users. For everyone else, it only shows public
        posts. Posts are sorted by counts of likes and comments and are ordered by
        creation date.
        """
        user = self.request.user
        search_term = self.request.query_params.get("search", "").strip()

        # Base queryset depending on user authentication
        if user.is_authenticated:
            queryset = Post.objects.filter(
                Q(is_private=False) |
                Q(owner=user) |
                Q(owner__followed__owner=user, is_private=True)
            )
            if 'owner__followed__owner__profile' in self.request.query_params:
                queryset = queryset.exclude(owner=user)
        else:
            queryset = Post.objects.filter(is_private=False)
    
        # Annotate likes and comments counts
        queryset = queryset.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True)
        ).order_by('-created_at')

        # Apply search filtering if search_term exists
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(artist_name__icontains=search_term) |
                Q(owner__username__icontains=search_term)
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            artist_name=serializer.validated_data.get('artist_name'),
            year_of_artwork=serializer.validated_data.get('year_of_artwork')
        )

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