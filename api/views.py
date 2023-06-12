from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PostSerializer
from .models import Post, User


class Login(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("email"), password=request.data.get("password"))
        if not user:
            return Response('Email or password is incorrect', status=HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=HTTP_200_OK)


class Register(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if len(User.objects.filter(email=email)) > 0:
            return Response('Email is already taken', status=HTTP_400_BAD_REQUEST)
        User.objects.create_user(username=email, email=email, password=password)
        return Response('Success!', status=HTTP_200_OK)


class Posts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        result = []
        for x in serializer.data:
            x = dict(x)
            print(x)
            if request.user in posts.get(pk=x["pk"]).liked_users.all():
                x["is_liked"] = True
            result.append(x)
        return Response(result, status=HTTP_200_OK)


class UserData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({'email': user.email}, HTTP_200_OK)


class MyPosts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        posts = user.post_set.all()
        serializer = PostSerializer(posts, many=True)
        result = []
        for x in serializer.data:
            x = dict(x)
            print(x)
            if user in posts.get(pk=x["pk"]).liked_users.all():
                x["is_liked"] = True
            result.append(x)
        return Response(result, status=HTTP_200_OK)

    def post(self, request):
        text = request.data.get("content")
        user = request.user
        post = Post(text=text, user=user)
        post.save()
        return Response('Created!', status=HTTP_200_OK)

    def put(self, request):
        try:
            user = request.user
            post_pk = request.data.get("post_pk")
            new_text = request.data.get("content")
            post = user.post_set.get(pk=post_pk)
            post.text = new_text
            post.save()
            return Response('Updated', status=HTTP_200_OK)
        except Exception as e:
            return Response('Error!', status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = request.user
            post_pk = request.data.get("post_pk")
            post = user.post_set.get(pk=post_pk)
            post.delete()
            serializer = PostSerializer(user.post_set.all(), many=True)
            result = []
            for x in serializer.data:
                x = dict(x)
                print(x)
                if user in user.post_set.all().get(pk=x["pk"]).liked_users.all():
                    x["is_liked"] = True
                result.append(x)
            return Response(result, status=HTTP_200_OK)
        except Exception as e:
            return Response('Error!', status=HTTP_400_BAD_REQUEST)


class LikePost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PostSerializer(user.liked_posts.all(), many=True)
        result = []
        for x in serializer.data:
            x = dict(x)
            print(x)
            if user in user.post_set.all().get(pk=x["pk"]).liked_users.all():
                x["is_liked"] = True
            result.append(x)
        return Response(result, status=HTTP_200_OK)
    def post(self, request):
        user = request.user
        post = Post.objects.get(pk=request.data.get('post_pk'))
        if user in post.liked_users.all():
            post.liked_users.remove(user)
        else:
            post.liked_users.add(user)
        return Response('Ok!', HTTP_200_OK)
