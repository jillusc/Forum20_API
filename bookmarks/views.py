from rest_framework import generics, permissions, status
from rest_framework.response import Response
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

    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        user = request.user
        existing_bookmark = Bookmark.objects.filter(post_id=post_id, owner=user).first()

            # if bookmark exists, remove it (toggle off)
        if existing_bookmark:
            existing_bookmark.delete()
            return Response({"detail": "bookmark removed"}, status=status.HTTP_204_NO_CONTENT)
            # otherwise, create new bookmark (toggle on)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Enables viewing of bookmarked posts, and deletion of 
    bookmarks only by their owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

