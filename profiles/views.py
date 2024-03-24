from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import generics, filters
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    Enables viewing of profiles. Profiles display counts of posts, followers
    and following and are ordered by creation date, newest first. Enables
    filtering by profiles followed by the authenticated user. Enables ordering
    by posts count, followers count, following count, and the creation date of
    follow relationships.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Enables detailed viewing of a profile, and updating and deletion of a
    profile only by its owner. Profiles display counts of posts, followers and
    following and are ordered by creation date, newest first.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
