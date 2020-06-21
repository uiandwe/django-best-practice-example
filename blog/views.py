from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .filters import PostFilter
from .models import Post
from .pagination import CustomMakePagination
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    pagination_class = CustomMakePagination
    filter_class = PostFilter

    ordering_fields = ["count", "public"]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
