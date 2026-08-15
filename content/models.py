from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F


class NewsItem(models.Model):
    slug = models.SlugField(unique=True, verbose_name='Link (slug)', help_text='Automatski se popunjava iz naslova. Koristi se u adresi stranice.')
    title = models.CharField(max_length=300, verbose_name='Naslov')
    excerpt = models.TextField(verbose_name='Kratak opis', help_text='Prikazuje se na početnoj stranici i u arhivi, ispod naslova.')
    date = models.DateField(verbose_name='Datum objave')
    thumbnail = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Naslovna fotografija', help_text='Glavna slika koja se prikazuje uz vijest.')
    content = models.TextField(blank=True, null=True, verbose_name='Tekst vijesti', help_text='Puni tekst koji se prikazuje na stranici vijesti.')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Vijest'
        verbose_name_plural = 'Vijesti'

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(NewsItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_gallery/', verbose_name='Fotografija')
    order = models.PositiveIntegerField(default=0, verbose_name='Redoslijed', help_text='Manji broj = prikazuje se prije.')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Fotografija'
        verbose_name_plural = 'Fotografije'

    def __str__(self):
        return f'Fotografija {self.order + 1}'


class ImportantLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='Naziv')
    url = models.URLField(blank=True, verbose_name='Veb adresa', help_text='Za link ka spoljnoj stranici (npr. sajt ministarstva).')
    file = models.FileField(upload_to='important_links/', blank=True, verbose_name='Fajl', help_text='Za dokument koji se otprema i čuva na našem sajtu (PDF i sl.). Popuni ili ovo, ili adresu iznad — ne oboje.')
    logo = models.ImageField(upload_to='important_links_logos/', blank=True, null=True, verbose_name='Logo', help_text='Logo institucije koji se prikazuje uz link.')
    order = models.PositiveIntegerField(default=0, verbose_name='Redoslijed', help_text='Manji broj = prikazuje se prije.')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Važan link'
        verbose_name_plural = 'Važni linkovi'

    def clean(self):
        if not self.url and not self.file:
            raise ValidationError('Unesite veb adresu ili otpremite fajl.')
        if self.url and self.file:
            raise ValidationError('Popunite samo jedno: veb adresu ili fajl, ne oboje.')

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=300, verbose_name='Naslov')
    excerpt = models.TextField(verbose_name='Tekst oglasa')
    date = models.DateField(blank=True, null=True, verbose_name='Datum objave', help_text='Ostavi prazno ako datum nije poznat — oglas će se prikazati bez datuma.')
    photo = models.ImageField(upload_to='oglasi/', blank=True, null=True, verbose_name='Fotografija')
    link = models.URLField(blank=True, verbose_name='Link', help_text='Opciono — npr. link za prijavu ili više informacija.')
    link_label = models.CharField(max_length=100, blank=True, verbose_name='Tekst linka', help_text='Npr. "Prijava putem portala eUprava". Ostavi prazno za podrazumijevani tekst.')
    is_open = models.BooleanField(default=True, verbose_name='Aktivan (otvoren)', help_text='Isključi kada rok istekne ili se pozicija popuni — oglas ostaje na sajtu, ali se označava kao "Isteklo".')

    class Meta:
        ordering = ['-is_open', F('date').desc(nulls_last=True), '-id']
        verbose_name = 'Oglas'
        verbose_name_plural = 'Oglasi'

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=200, verbose_name='Naziv')
    url = models.URLField(verbose_name='Veb adresa')
    logo = models.ImageField(upload_to='members/', blank=True, null=True, verbose_name='Logo')

    class Meta:
        ordering = ['name']
        verbose_name = 'Član'
        verbose_name_plural = 'Članovi'

    def __str__(self):
        return self.name
