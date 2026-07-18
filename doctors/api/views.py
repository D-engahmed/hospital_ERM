from rest_framework import viewsets, permissions
from doctors.models import Category, Blogs, Comments
from .serializers import CategorySerializer, BlogSerializer, CommentSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blogs.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['title', 'description']
    ordering_fields = ['posted_at']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
