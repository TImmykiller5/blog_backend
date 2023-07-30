from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializerWithToken, BlogPostSerializers, GetPostSerializers, CommentSerializer
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from django.contrib.auth.models import User
# Create your views here.


class MyTOkenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'username or password is incorrect!'}

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        # data['username'] = self.user.username

        for k, v in serializer.items():
            data[k] = v

        return data


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTOkenObtainPairSerializer


class test(APIView):
    def get(self, request):
        return Response({'detail': 'yes i function'})


class registerUser(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User(
                first_name=data['email'],
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
            serializer = UserSerializerWithToken(user, many=False)
            user.save()
            return Response(serializer.data)

        except:
            message = {
                'detail': 'USER WITH THIS EMAIL OR USERNAME ALREADY EXIST'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class getPosts(APIView):
    def get(self, request):
        posts = BlogPost.objects.all()
        serialzer = BlogPostSerializers(posts, many=True)
        return Response(serialzer.data)


class getPost(APIView):
    def get(self, request, pk):
        posts = BlogPost.objects.get(id=pk)
        serialzer = GetPostSerializers(posts, many=False)
        return Response(serialzer.data)


# class editPost(APIView):



class createPost(APIView):
    permission_classes = [IsAuthenticated]


    def put(self, request, pk):
        owner = request.user
        data = request.data
        # print(data)
        tags = data['tag']

        id = pk
        blog = BlogPost.objects.filter(owner=owner).filter(id = id)
        if len(blog) > 0 :
            blog = blog[0]
            blog.title= data['title']
            blog.text= data['text']
            blog.save()
            for tag in tags:
                check = Tags.objects.filter(tagName=tag)
                lenght = (len(check))
                if lenght == 0:
                    newtag = Tags(tagName=tag)
                    newtag.save()
                    blog.tag.add(newtag)

                else:
                    newtag = check[0]
                    blog.tag.add(newtag)
            blog.save()
        else:
            message = {'detail': 'this action cannot be completed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetPostSerializers(blog, many=False)
        return Response(serializer.data)
        
   

    def post(self, request):
        user = request.user
        data = request.data
        tags = data['tag']

        print(tags)
        posts = BlogPost(
            title=data['title'],
            text=data['text'],
            owner=user
        )

        posts.save()
        print(type(tags))
        for tag in tags:
            print(tag)
            check = Tags.objects.filter(tagName=tag)
            # print(check)
            lenght = (len(check))
            if lenght == 0:
                newtag = Tags(tagName=tag)
                newtag.save()
                posts.tag.add(newtag)

            else:
                newtag = check[0]
                posts.tag.add(newtag)

                # print(newtag.id)

        posts.save()

        serialzer = GetPostSerializers(posts, many=False)
        # print(serialzer.data)
        return Response(serialzer.data)
        # return Response({'hi':'hello'})

class getOwnerPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = request.user
        print(request)
        posts = BlogPost.objects.filter(owner=owner)
        serialzer = BlogPostSerializers(posts, many=True)
        return Response(serialzer.data)

class deletePost(APIView):
    permission_classes =[IsAuthenticated]

    def delete(self, request, pk):
        owner = request.user
        id = pk
        blog = BlogPost.objects.filter(owner=owner).filter(id = id)
        print(blog)
        blog.delete()
        
        return Response({'deleted':'true'})
    
class commentHadler(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        owner = request.user
        id = pk
        data = request.data
        blog = BlogPost.objects.get(id=id)
        comment = Comment(
            text=data['text'],
            blog = blog,
            owner = owner
        )

        comment.save()
        comments = blog.comment_set.all().order_by('-id')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)