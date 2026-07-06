from pathlib import Path

from django.contrib.auth.models import User
from django.db.utils import OperationalError, ProgrammingError
from django.core.files import File
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from rewear.management.commands.seed_sample_data import ITEM_SPECS, SEED_USERS
from rewear.models import Item


class Command(BaseCommand):
    help = "Restore bundled sample product images into the active Django media storage."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite image files even when an item already has an image path.",
        )

    def handle(self, *args, **options):
        assets_dir = Path(__file__).resolve().parents[2] / "sample_media" / "items"
        force = options["force"]
        restored = 0
        skipped = 0
        missing = []
        user_emails = {user["name"]: user["email"] for user in SEED_USERS}

        if not assets_dir.exists():
            self.stdout.write(self.style.ERROR(f"Bundled sample image directory not found: {assets_dir}"))
            return

        try:
            for spec in ITEM_SPECS:
                owner_email = user_emails.get(spec["owner"])
                try:
                    owner = User.objects.get(email=owner_email)
                    item = Item.objects.get(owner=owner, title=spec["title"])
                except (User.DoesNotExist, Item.DoesNotExist):
                    missing.append(f'{spec["owner"]} / {spec["title"]} (missing user or item)')
                    continue

                image_field = item.image
                image_exists = bool(image_field and image_field.name and image_field.storage.exists(image_field.name))
                if image_exists and not force:
                    skipped += 1
                    continue

                base_name = f'{slugify(spec["owner"])}-{slugify(spec["title"])}'
                source_path = self._find_source_file(assets_dir, base_name)
                if source_path is None:
                    missing.append(f'{spec["owner"]} / {spec["title"]} (missing asset file)')
                    continue

                with source_path.open("rb") as source_handle:
                    image_field.save(source_path.name, File(source_handle), save=True)
                restored += 1
        except (OperationalError, ProgrammingError) as exc:
            self.stdout.write(
                self.style.ERROR(
                    "Database tables are not ready yet. Run migrations first, and seed the sample data before "
                    f"restoring images. Original error: {exc}"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample image restore completed: {restored} restored, {skipped} skipped, {len(missing)} missing."
            )
        )
        for entry in missing:
            self.stdout.write(self.style.WARNING(f"- {entry}"))

    def _find_source_file(self, assets_dir: Path, base_name: str) -> Path | None:
        for extension in (".jpg", ".jpeg", ".png", ".webp"):
            candidate = assets_dir / f"{base_name}{extension}"
            if candidate.exists():
                return candidate
        return None
