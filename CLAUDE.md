# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Boardgame Rank (`bg_rank`) — a Django app for registering boardgame matches, seasons, and player rankings.

## Development environment

This repo is designed to run inside the devcontainer defined in `.devcontainer/devcontainer.json` (built from `deployment/local/Dockerfile` via `deployment/local/docker-compose.yml`). The container installs Python, Node, the AWS CLI, and AWS CDK, and runs `pre-commit install` on start. The devcontainer sets the VS Code terminal cwd to `/workspace/app/src/bg_rank` — most commands below assume that directory.

The container also writes env vars from `.aws_credentials/` and `.django_settings/` into `~/.bashrc` via `tasks.py`'s `invoke update-bashrc` task (see `Dockerfile`). Notably `DJANGO_SECRET_KEY` and `DJANGO_IS_DEVELOP` come from `.django_settings/settings` — both dirs are gitignored and must exist locally/be mounted for the app to boot.

## Commands

Run from `app/src/bg_rank/` (the Django project root, containing `manage.py`):

```bash
# run dev server
python manage.py runserver

# migrations
python manage.py makemigrations
python manage.py migrate

# tests (per-app, Django's test runner)
python manage.py test dashboard
python manage.py test login
python manage.py test dashboard.tests.<TestClassName>.<test_method_name>

# create a superuser
python manage.py createsuperuser
```

Dependencies are split across three requirement files that layer on each other:
- `app/requirements.txt` — CDK/infra deps (`aws-cdk-lib`, `constructs`, `pyyaml`) used for deployment tooling, not the Django app itself.
- `app/requirements-dev.txt` — dev/test deps (`pytest`).
- `deployment/local/requirements.txt` — the actual Django app deps (Django, `django-select2`, `invoke`, `pre-commit`, `detect-secrets`); it `-r`-includes both files above. Install with `pip install -r deployment/local/requirements.txt`.

Linting/formatting is via `ruff` (pre-commit hook, `--fix` + `ruff-format`); secret scanning is via `detect-secrets` against `.secrets.baseline`. Both run through `pre-commit run --all-files`.

## Architecture

Django project root is `app/src/bg_rank/` (project package `bg_rank/`, apps `dashboard/` and `login/`).

- **`login` app** — authentication only: login, registration (`CustomUserCreationForm` extends Django's `UserCreationForm` with password confirmation), using Django's built-in `User` model. No custom user model.
- **`dashboard` app** — the actual product: `Boardgame`, `Season`, `Match` models, plus `MatchPlayer`/`SeasonPlayer` through-models joining `User` to matches/seasons with per-player scores.
  - `BGModel` (abstract base in `dashboard/models.py`) auto-generates a unique `slug` from `slug_source_field` (default `"name"`) on save if the slug is blank, appending `-1`, `-2`, etc. on collision. All content models (`Boardgame`, `Season`, `Match`) inherit from it.
  - `SeasonPlayer` computes `score`, `average_score`, and `match_count` as properties that aggregate over `MatchPlayer` filtered by `season_id` — these are derived, not stored.
  - Views are a mix of function-based (`main`, `match`, `season`) and class-based (`FormView` for create flows, `ListView`/`DetailView` for listing/detail, `LoginRequiredMixin` for profile pages). Forms for `Match`/`Season` use `django_select2`'s `ModelSelect2MultipleWidget` (`PlayerWidget` in `dashboard/forms.py`) for the `enrolled_players` multi-select against `User`.
- Root URLconf (`bg_rank/urls.py`) mounts `login.urls` and `dashboard.urls` at `""`, plus `/admin/` and `/select2/`.
- Templates: project-wide base templates in `app/src/bg_rank/templates/`; per-app templates under each app's `templates/<app_name>/`.
- Settings (`bg_rank/settings.py`) reads `DJANGO_SECRET_KEY` and `DJANGO_IS_DEVELOP` from the environment; DB is SQLite at `bg_rank/db.sqlite3` (gitignored). `LANGUAGE_CODE` is `pt-br` — user-facing strings (labels, messages) are written in Portuguese.
- `docs/sitemap.md` has a mermaid diagram of the app's page/navigation structure (Login → Main → Players/Boardgames/Season/Matches, plus Profile).

## Notes

- `utils/utils.py` exists but is currently empty.
- `tasks.py` (repo root) defines an `invoke` task, `update-bashrc`, used only during the container build to flatten INI-style credential/settings files into environment variables — not part of the app runtime.
