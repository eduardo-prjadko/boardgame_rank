from django.db import models
from django.utils.text import slugify


class Boardgame(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Season(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start_at = models.DateField()
    end_at = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Match(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    boardgame_id = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True)
    season_id = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    is_friendly = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.is_friendly = False if self.season_id is not None else True
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
