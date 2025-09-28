from rest_framework import generics, permissions, status
from rest_framework.response import Response
from Forum20_API.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    Enables viewing of likes, and adding of likes only by logged-in users.
    Likes are assigned to the currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get_queryset(self):
        return Like.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        post = request.data.get('post')
        user = request.user
        existing_like = Like.objects.filter(post_id=post, owner=user).first()

            # if Like exists, remove it (toggle off)
        if existing_like:
            existing_like.delete()
            return Response({'detail': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
            # otherwise, create a new Like (toggle on)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Enables viewing of likes, and deletion of likes only by their owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
