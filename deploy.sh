#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ───────────────────────────────────────────────
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRANCH="dev"

echo "=== Deploying lesson_schedule_assistant (branch: $BRANCH) ==="

# ── Pull latest code ────────────────────────────────────────────
cd "$PROJECT_DIR"
git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"

# ── Backend ─────────────────────────────────────────────────────
echo "--- Backend: installing dependencies ---"
cd "$PROJECT_DIR/backend"

uv venv --python python3 .venv 2>/dev/null || true
uv pip install -r requirements.txt --python .venv/bin/python

echo "--- Backend: running migrations ---"
.venv/bin/python manage.py migrate --noinput

echo "--- Backend: collecting static files ---"
.venv/bin/python manage.py collectstatic --noinput

# ── Bot ─────────────────────────────────────────────────────────
echo "--- Bot: installing dependencies ---"
cd "$PROJECT_DIR/bot"

uv venv --python python3 .venv 2>/dev/null || true
uv pip install -r requirements.txt --python .venv/bin/python

# ── Restart services ────────────────────────────────────────────
echo "--- Restarting services ---"
sudo systemctl restart lesson-backend.service  || echo "WARNING: could not restart lesson-backend"
sudo systemctl restart lesson-bot.service      || echo "WARNING: could not restart lesson-bot"

echo "=== Deployment complete ==="
