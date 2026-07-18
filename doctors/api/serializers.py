from rest_framework import serializers
from doctors.models import Category, Blogs, Comments
from users.api.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='id_category', read_only=True)
    author_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = Blogs
        fields = ['blog_id', 'title', 'summary', 'description', 'is_published', 'posted_at', 'thumbnail', 'category', 'author_name']
        read_only_fields = ['blog_id', 'posted_at']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comments
        fields = ['comment_id', 'content', 'commented_at', 'username', 'blog']
        read_only_fields = ['comment_id', 'commented_at']
