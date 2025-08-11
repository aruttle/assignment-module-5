#!/usr/bin/env bash
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser automatically if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "ChangeMe123")
    print("Superuser 'admin' created.")
else:
    print("Superuser 'admin' already exists.")
EOF

# Collect static files
python manage.py collectstatic --noinput
