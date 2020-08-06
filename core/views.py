from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .tasks import parse_habr


class Runner(APIView):
    def get(self, request):
        parse_habr.delay()
        return Response({"response": "ok"})
