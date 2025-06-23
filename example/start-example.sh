#! /usr/bin/env bash
export DJANGO_SUPERUSER_PASSWORD=admin
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@admin.com

# First Migration to ensure database is set up and create user
python manage.py migrate

# Create a superuser if it does not already exist
# Check if the superuser already exists
USER_EXISTS=$(python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())
" 2>/dev/null)

if [ "$USER_EXISTS" != "True" ]; then
    echo "Creating superuser..."
    if ! python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"; then
        echo "Error: Failed to create superuser." >&2
        exit 1
    fi
else
    echo "Superuser already exists."
fi

python manage.py runserver 0.0.0.0:8080
