from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_image = serializers.ImageField(source='post.image', read_only=True)
    post_owner = serializers.ReadOnlyField(source='post.owner.username')
    post_owner_avatar = serializers.ReadOnlyField(source='post.owner.profile.image.url')
    
    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post', 'post_title', 'post_image', 'post_owner', 'post_owner_avatar']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })