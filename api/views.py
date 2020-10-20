from .models import *
import jwt
from django.conf import settings
from .serializers import *
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status
from rest_framework import generics
from rest_framework.response import Response
from django.http import Http404
from django.contrib.postgres.search import SearchVector
from tokens import user_token
from rest_framework.permissions import IsAuthenticated


# Регистрация пользователя
class RegisterUser(APIView):

	def post(self, request):
		serializer = UserdSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Авторизация пользователя
class JSONWebTokenAuth(APIView):
	throttle_classes = ()
	permission_classes = ()
	parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
	renderer_classes = (renderers.JSONRenderer,)
	serializer_class = AuthSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			print(serializer)
			user = serializer.validated_data['login']
			token = jwt.encode({
				'pk': user,
			}, settings.SECRET_KEY)
			user_token[token] = token
			return Response({'token': token})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Добавление статьи
class AddPostView(APIView):
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Редактирование и удаление публикации
class PostView(APIView):
	permission_classes = [IsAuthenticated]

	def get_object(self, pk):
		try:
			return Post.objects.get(pk=pk)
		except Post.DoesNotExist:
			raise Http404

	def put(self, request, pk):
		post = self.get_object(pk)
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		post = self.get_object(pk)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


# Сортировка
class SortedAndFilterPostViews(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self, **kwargs):
		print(**kwargs)
		if self.request.GET.get('sorting'):
			keyword = self.request.GET.get('sorting')
			if keyword:
				if keyword == "1":
					queryset = Post.objects.order_by('pk')
				elif keyword == "-1":
					queryset = Post.objects.order_by('-pk')
				else:
					queryset = Post.objects.all()
				return queryset
		elif self.request.GET.get('answer'):
			keyword = self.request.GET.get('answer')
			if keyword is not None:
				queryset = Post.objects.annotate(search=SearchVector('name', 'body')).filter(search=keyword)
				return queryset
		elif self.request.GET.get('city'):
			keyword = self.request.GET.get('city')
			if keyword is not None:
				queryset = Post.objects.filter(city__name=keyword)
				return queryset
		else:
			queryset = Post.objects.all()
			return queryset
