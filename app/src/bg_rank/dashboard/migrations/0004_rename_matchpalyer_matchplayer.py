# Generated by Django 5.2.1 on 2025-06-10 21:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_alter_matchpalyer_score"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MatchPalyer",
            new_name="MatchPlayer",
        ),
    ]
