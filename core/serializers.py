from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["pk", "url", "title", "abstract", "created_at"]


class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["pk", "url", "title", "body", "created_at"]
