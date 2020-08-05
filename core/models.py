from django.db import models


class Article(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=1024)
    body = models.TextField()

    @property
    def abstract(self):
        return self.body[:700]
