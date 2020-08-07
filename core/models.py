from django.db import models


class Article(models.Model):
    """Модель статьи на Хабре."""
    url = models.URLField(unique=True)
    title = models.CharField(max_length=1024)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def abstract(self):
        """Краткое содержание, первые 700 символов тела статьи."""
        return str(self.body[:700])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
