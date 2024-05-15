from rest_framework import generics, permissions
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkList(generics.ListCreateAPIView):
    """
    Enables viewing of bookmarked posts, and adding of bookmarks
    only by logged-in users. Bookmarks are assigned to the
    currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)

class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Enables viewing of bookmarked posts, and deletion of 
    bookmarks only by their owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

