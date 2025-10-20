from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post_id = serializers.ReadOnlyField(source='post.id')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_image = serializers.ImageField(source='post.image', read_only=True)
    post_owner = serializers.ReadOnlyField(source='post.owner.username')
    post_owner_avatar = serializers.ReadOnlyField(source='post.owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post',  'post_id', 'post_title', 'post_image', 'post_owner', 'post_owner_avatar', 'created_at', 'updated_at', 'content'
        ]
        read_only_fields = ['created_at', 'updated_at']



class CommentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    post = serializers.ReadOnlyField(source='post.id')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_image = serializers.ImageField(source='post.image', read_only=True)
    post_owner = serializers.ReadOnlyField(source='post.owner.username')
    post_owner_avatar = serializers.ReadOnlyField(source='post.owner.profile.image.url')


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post', 'post_title', 'post_image', 'post_owner', 'post_owner_avatar', 'created_at', 'updated_at', 'content'
        ]
        read_only_fields = ['created_at', 'updated_at']
