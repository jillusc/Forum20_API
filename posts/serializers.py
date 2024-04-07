from rest_framework import serializers
from posts.models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_private = serializers.BooleanField(required=False)
    image = serializers.ImageField(required=False)
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Please upload an image.")
        if hasattr(value, 'size'):
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                'Image size must be max. 2MB!')
            if value.image.height > 4096:
                raise serializers.ValidationError(
                'Image height must be max. 4096px!')
            if value.image.width > 4096:
                raise serializers.ValidationError(
                'Image width must be max. 4096px!')
        else:
            return value
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'like_id', 'likes_count', 'comments_count', 'is_private',
        ]
