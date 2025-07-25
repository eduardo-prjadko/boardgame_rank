from django.db import models
from django.contrib.auth.models import User


# class BGModel(models.Model):
#     slug_source_field = "name"  # Default source field for slug

#     slug = models.SlugField(unique=True, blank=True)

#     class Meta:
#         abstract = True  # This is an abstract base class

#     def save(self, *args, **kwargs):
#         # Only auto-slug if slug is blank and the source field exists
#         if not self.slug and hasattr(self, self.slug_source_field):

#             base_slug = slugify(getattr(self, self.slug_source_field))
#             slug = base_slug
#             counter = 1
#             ModelClass = self.__class__
#             while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1
#             self.slug = slug
#         super().save(*args, **kwargs)


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
    enrolled_players = models.ManyToManyField(User, through="SeasonPlayer")
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
    enrolled_players = models.ManyToManyField(User, through="MatchPlayer")
    is_friendly = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class MatchPlayer(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "match"], name="unique_match_player"
            )
        ]


class SeasonPlayer(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    @property
    def score(self):
        return (
            MatchPlayer.objects.filter(
                player=self.player, match__season_id=self.season
            ).aggregate(total=models.Sum("score"))["total"]
            or 0.0
        )

    @property
    def average_score(self):
        result = MatchPlayer.objects.filter(
            player=self.player, match__season_id=self.season
        ).aggregate(avg=models.Avg("score"))["avg"]
        return result or 0.0

    @property
    def match_count(self):
        return MatchPlayer.objects.filter(
            player=self.player, match__season_id=self.season
        ).count()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "season"], name="unique_season_player"
            )
        ]
