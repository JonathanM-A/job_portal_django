from typing import Any
from django.core.management.base import BaseCommand
from permissions.models import create_groups_and_permissions

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        create_groups_and_permissions()