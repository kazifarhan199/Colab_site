from django.db import models
from django.contrib.auth import get_user_model
from tinymce import HTMLField
from tinymce import TinyMCE

class Projects_model(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 400)
    body = HTMLField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

