import os
import subprocess


def tests() -> None:
    command = [
        "pytest",
        "-n",
        "auto",
        "--doctest-modules",
        "--cov=admin_shelf",
        "--cov-report=term",
        "--cov-report=html:htmlcov",
        "--cov-report=xml:coverage.xml",
    ]
    subprocess.run(" ".join(command), shell=True, check=True)  # noqa: S602


def example() -> None:
    django_superuser_username = "admin"
    django_superuser_email = "admin@admin.com"
    os.environ["DJANGO_SUPERUSER_USERNAME"] = django_superuser_username

    # First Migration to ensure database is set up and create user
    migrate_command = [
        "python",
        "manage.py",
        "migrate",
    ]
    subprocess.run(" ".join(migrate_command), shell=True, check=True)  # noqa: S602

    # Then we check if the superuser already exists
    user_exists_command = [
        "python",
        "manage.py",
        "shell",
        "-c",
        f'"from django.contrib.auth import get_user_model; User = get_user_model(); '
        f"print(User.objects.filter(username='{django_superuser_username}').exists())\"",
    ]

    print(" ".join(user_exists_command))
    user_exists = (
        subprocess.run(  # noqa: S602
            " ".join(user_exists_command),
            shell=True,
            check=True,
            capture_output=True,
        )
        .stdout.decode()
        .strip()
    )
    if "True" not in user_exists:
        # If the superuser does not exist, we create it
        create_superuser_command = [
            "python",
            "manage.py",
            "createsuperuser",
            "--noinput",
            "--username",
            django_superuser_username,
            "--email",
            django_superuser_email,
        ]
        subprocess.run(  # noqa: S602
            " ".join(create_superuser_command), shell=True, check=True
        )
    else:
        print("Superuser already exists.")

    # Finally, we run the server
    runserver_command = [
        "python",
        "manage.py",
        "runserver",
        "0.0.0.0:8080",
    ]
    subprocess.run(" ".join(runserver_command), shell=True, check=True)  # noqa: S602
