from django.db import models


class Article(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=1024)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def abstract(self):
        return self.body[:700]
