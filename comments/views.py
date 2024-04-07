from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    """
    Enables viewing of comments, and creation of comments only by logged-in
    users. Enables filtering by posts. New comments are assigned to the
    currently authenticated user. Allows for filtering of comments that
    belong to the authenticated user. 
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('user_comments') == 'true':
            return queryset.filter(owner=self.request.user)
        return queryset


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Enables detailed viewing of a comment, and updating and deletion of a
    comment only by its owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
