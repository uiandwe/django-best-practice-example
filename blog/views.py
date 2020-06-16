from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomResultsSetPagination, CustomMakePagination


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    pagination_class = CustomMakePagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
