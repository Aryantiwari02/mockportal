#!/usr/bin/env bash
# ============================================================
# YojanaSaathi backend — production build script
# Works on Render, Railway, Heroku-style and most PaaS hosts.
# ============================================================
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Collect Django/DRF/admin static files for WhiteNoise to serve
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Seed demonstration schemes (idempotent — safe to run on every deploy)
python manage.py seed_schemes
