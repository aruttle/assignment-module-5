#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser automatically if it doesn't exist (CustomUser uses email)
python manage.py shell <<'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
email = "alruttle@gmail.com.com"
password = "ChangeMe123"
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print("Superuser created:", email)
else:
    print("Superuser already exists:", email)
EOF

# Collect static files
python manage.py collectstatic --noinput
