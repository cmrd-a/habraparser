from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Article
from .serializers import ArticleSerializer, ArticleDetailsSerializer
from .tasks import parse_daily, parse_post


class ArticleSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    pagination_class = ArticleSetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleDetailsSerializer
        return ArticleSerializer


class ForceParsing(APIView):
    """API для ручного запуска парсинга."""

    def get(self, request):
        """Выполнит полный парсинг лучший статей за день."""
        task = parse_daily.delay()
        return Response({"Task ID": task.id})

    def post(self, request):
        """Парсинг конкретной статьи по переданному url."""
        url = str(request.data.get("url", None))
        task = parse_post.delay(url)
        return Response({"Task ID": task.id})
