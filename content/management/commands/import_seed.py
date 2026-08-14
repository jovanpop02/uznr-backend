import json
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from content.models import ImportantLink, Member, NewsImage, NewsItem

DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'seed_data'


def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def filename_from_url(url):
    return Path(urlparse(url).path).name or 'file'


class Command(BaseCommand):
    help = 'Import seed news/members JSON (with real scraped image URLs) into the database.'

    def handle(self, *args, **options):
        # Members/links are cheap (no per-item image downloads to wait on) and
        # matter for the homepage sidebar/members section, so seed them before
        # news, whose thumbnail/gallery downloads can take a long time and
        # must never block the rest of the seed from running.
        for step in (self.import_members, self.import_important_links, self.import_news):
            try:
                step()
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f'{step.__name__} failed: {exc}'))

    def import_news(self):
        path = DATA_DIR / 'news.json'
        items = json.loads(path.read_text(encoding='utf-8'))
        created = 0
        for item in items:
            obj, _ = NewsItem.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'excerpt': item['excerpt'],
                    'date': item['date'],
                    'content': item.get('content'),
                },
            )
            if item.get('thumbnail') and not obj.thumbnail:
                try:
                    data = download(item['thumbnail'])
                    obj.thumbnail.save(filename_from_url(item['thumbnail']), ContentFile(data), save=True)
                except Exception as exc:
                    self.stderr.write(f"  thumbnail failed for {item['slug']}: {exc}")
            gallery = item.get('images') or []
            if gallery and not obj.images.exists():
                for order, url in enumerate(gallery):
                    try:
                        data = download(url)
                        img = NewsImage(news=obj, order=order)
                        img.image.save(filename_from_url(url), ContentFile(data), save=True)
                    except Exception as exc:
                        self.stderr.write(f"  gallery image failed for {item['slug']} ({url}): {exc}")
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {created} news items'))

    def import_members(self):
        path = DATA_DIR / 'members.json'
        items = json.loads(path.read_text(encoding='utf-8'))
        created = 0
        for item in items:
            obj, _ = Member.objects.update_or_create(
                name=item['name'],
                defaults={'url': item['url']},
            )
            if item.get('logo') and not obj.logo:
                try:
                    data = download(item['logo'])
                    obj.logo.save(filename_from_url(item['logo']), ContentFile(data), save=True)
                except Exception as exc:
                    self.stderr.write(f"  logo failed for {item['name']}: {exc}")
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {created} members'))

    def import_important_links(self):
        path = DATA_DIR / 'important_links.json'
        if not path.exists():
            return
        items = json.loads(path.read_text(encoding='utf-8'))
        created = 0
        for item in items:
            ImportantLink.objects.update_or_create(
                title=item['title'],
                defaults={'url': item.get('url', ''), 'order': item.get('order', 0)},
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {created} important links'))
