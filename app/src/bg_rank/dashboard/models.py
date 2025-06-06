from django.db import models


class Boardgame(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Season(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start_at = models.DateField()
    end_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Match(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    boardgame_id = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True)
    season_id = models.ForeignKey(
        Season, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_friendly = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
