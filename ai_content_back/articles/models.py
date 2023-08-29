from django.db import models

# Create your models here.
class Article(models.Model):
    """Article model with title, date, source, body and read count fields. """

    title = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)
    source = models.CharField(max_length=200, blank=True)
    paragraph_one = models.TextField(blank=True)
    paragraph_two = models.TextField(blank=True)
    read_count = models.IntegerField(blank=True, null=True, default=0)
    image_url = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title}"
