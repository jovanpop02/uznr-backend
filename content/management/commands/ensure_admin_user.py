"""Creates the admin account from environment variables at boot.

Render's free plan has no shell, so `createsuperuser` cannot be typed anywhere.
This runs as part of the start command instead and reads the credentials from
the service's environment, where they belong anyway.

    ADMIN_USERNAME   required — without it the command does nothing
    ADMIN_PASSWORD   required
    ADMIN_EMAIL      optional
    ADMIN_READONLY   "True" (default) for an account that can look but not
                     touch; "False" for a full superuser

Read-only is the default on purpose. This database is rebuilt from the seed
files on every deploy, so anything typed into the live admin is lost the next
time the service restarts — an account that cannot save is an honest match for
storage that cannot keep. Set ADMIN_READONLY=False once the site has a real
database.

Idempotent: it resets the password and the permissions of an existing account
rather than failing, so a changed environment variable takes effect on the next
deploy.
"""

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Pravi administratorski nalog iz env varijabli (za servise bez shell-a).'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()
        email = os.environ.get('ADMIN_EMAIL', '').strip()
        readonly = os.environ.get('ADMIN_READONLY', 'True') != 'False'

        if not username or not password:
            self.stdout.write(
                'ADMIN_USERNAME/ADMIN_PASSWORD nisu postavljeni — nalog se ne pravi.'
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username, defaults={'email': email}
        )

        user.email = email or user.email
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = not readonly
        user.save()

        # A superuser bypasses the permission table entirely, so the explicit
        # grants below are only meaningful for the read-only case.
        user.user_permissions.clear()
        if readonly:
            user.user_permissions.set(
                Permission.objects.filter(
                    codename__startswith='view_',
                    content_type__app_label='content',
                )
            )

        role = 'samo pregled' if readonly else 'puna prava'
        state = 'napravljen' if created else 'ažuriran'
        self.stdout.write(
            self.style.SUCCESS(f'Nalog „{username}“ {state} ({role}).')
        )
