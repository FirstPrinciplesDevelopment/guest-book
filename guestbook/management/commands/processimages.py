from django.core.management.base import BaseCommand, CommandError
import os
from django.conf import settings
from guestbook.models import AvatarImage


class Command(BaseCommand):
    help = "Processes images for avatars."

    def build_url(self, filename):
        # TODO: update to be whatever the deployed URL will be.
        return os.path.join("/static", "guestbook", "images", filename)

    def handle(self, *args, **options):
        try:
            # Delete all images.
            AvatarImage.objects.all().delete()
            image_dir = os.path.join(
                settings.BASE_DIR, "guestbook", "static", "guestbook", "images"
            )
            for triple in os.walk(image_dir):
                # Unpack 3-tuple of dirpath, dirnames, filenames.
                (dirpath, _, filenames) = triple
                for filename in filenames:
                    # TODO: update to be whatever the deployed URL will be.
                    file_url = self.build_url(filename)
                    self.stdout.write(self.style.SUCCESS(f"Saving {file_url}"))
                    # Save to the database.
                    image = AvatarImage(url=file_url)
                    image.save()

        except:
            raise CommandError("Error processing images.")
