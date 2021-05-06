from django.db import models
from django.contrib.auth.models import User


class Me(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                related_name='users', null=True)

    # additional items
    profile_pic = models.ImageField(upload_to="my_pics", blank=True, null=True)
    background_pic = models.ImageField(
        upload_to="my_pics", blank=True, null=True)
    about_me = models.TextField()

    class Meta:
        verbose_name = "Me"
        verbose_name_plural = "Me"

    def __str__(self):
        return self.user.username

    @property
    def profileURL(self):
        try:
            url = self.profile_pic.url
        except ValueError:
            url = ''
        return url

    @property
    def backgroundURL(self):
        try:
            url_back = self.background_pic.url
        except ValueError:
            url_back = ''
        return url_back


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    software_used = models.CharField(max_length=200)
    project_image = models.ImageField(
        upload_to="project_images", blank=True, null=True)
    url = models.URLField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    @property
    def ImageURL(self):
        try:
            url = self.project_image.url
        except ValueError:
            url = ''
        return url



