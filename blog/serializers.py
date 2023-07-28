from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class TestSerializer(serializers.Serializer):
    pass

class UserSerializers(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class UserSerializerWithToken(UserSerializers):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'is_staff', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        
        return str(token.access_token)
    

class BlogPostSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only = True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model =BlogPost
        fields = ['id', 'title', 'text', 'created_at', 'updated_at', 'user', 'tags']

    def get_user(self, obj):
        user = obj.owner
        return user.username
    
    def get_tags(self, obj):
        tags = []
        for t in obj.tag.all():
            tags.append(str(t))
        return(tags)
    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at',  'user']
    
    def get_user (self, obj):
        return  obj.owner.username
    
    


class GetPostSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only = True)
    tags = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =BlogPost
        fields = ['id', 'title', 'text', 'created_at', 'updated_at', 'user', 'tags', 'comments']

    def get_user(self, obj):
        user = obj.owner
        return user.username
    
    def get_tags(self, obj):
        tags = []
        for t in obj.tag.all():
            tags.append(str(t))
        return(tags)
    
    def get_comments(self, obj):
        comments = obj.comment_set.all().order_by('-id')
        serializer = CommentSerializer(comments, many=True)
        return (serializer.data)