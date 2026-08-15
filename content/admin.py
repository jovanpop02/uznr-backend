from django.contrib import admin
from django.utils.html import format_html

from .models import Announcement, AnnouncementLink, ImportantLink, Member, NewsImage, NewsItem


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('preview', 'image', 'order')
    readonly_fields = ('preview',)
    classes = ('news-gallery-inline',)

    @admin.display(description='')
    def preview(self, obj):
        if not obj.pk or not obj.image:
            return ''
        return format_html(
            '<img src="{}" class="gallery-thumb" alt="" />', obj.image.url
        )


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'date')
    list_display_links = ('thumb', 'title')
    list_filter = ('date',)
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-date',)
    inlines = [NewsImageInline]

    fieldsets = (
        ('Osnovni podaci', {
            'fields': ('title', 'slug', 'date'),
        }),
        ('Sadržaj', {
            'fields': ('excerpt', 'content'),
        }),
        ('Naslovna fotografija', {
            'fields': ('thumbnail',),
        }),
    )

    @admin.display(description='')
    def thumb(self, obj):
        if not obj.thumbnail:
            return '—'
        return format_html('<img src="{}" class="list-thumb" alt="" />', obj.thumbnail.url)


class AnnouncementLinkInline(admin.TabularInline):
    model = AnnouncementLink
    extra = 1
    fields = ('title', 'url', 'file', 'order')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'status', 'date', 'order')
    list_display_links = ('thumb', 'title')
    list_filter = ('is_open', 'date')
    search_fields = ('title', 'excerpt')
    ordering = ('order', 'id')
    inlines = [AnnouncementLinkInline]

    fieldsets = (
        ('Osnovni podaci', {
            'fields': ('title', 'date', 'is_open', 'order'),
        }),
        ('Sadržaj', {
            'fields': ('excerpt', 'photo'),
        }),
        ('Istaknuti link u tekstu (opciono)', {
            'fields': ('link', 'link_label'),
            'description': 'Za jednu riječ/frazu koja postaje link unutar teksta oglasa (npr. "eUprave").',
        }),
    )

    @admin.display(description='')
    def thumb(self, obj):
        if not obj.photo:
            return '—'
        return format_html('<img src="{}" class="list-thumb" alt="" />', obj.photo.url)

    @admin.display(description='Status')
    def status(self, obj):
        if obj.is_open:
            return format_html('<span style="color: #2f8f45; font-weight: 600;">Otvoreno</span>')
        return format_html('<span style="color: #6b7a72;">Isteklo</span>')


@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ('logo_thumb', 'title', 'destination', 'order')
    list_display_links = ('title',)
    ordering = ('order', 'id')

    @admin.display(description='')
    def logo_thumb(self, obj):
        if not obj.logo:
            return '—'
        return format_html('<img src="{}" class="list-thumb list-thumb--logo" alt="" />', obj.logo.url)

    @admin.display(description='Vodi na')
    def destination(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Fajl ↗</a>', obj.file.url)
        if obj.url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url)
        return '—'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('logo_thumb', 'name', 'url')
    list_display_links = ('logo_thumb', 'name')
    search_fields = ('name',)
    ordering = ('name',)

    @admin.display(description='')
    def logo_thumb(self, obj):
        if not obj.logo:
            return '—'
        return format_html('<img src="{}" class="list-thumb list-thumb--logo" alt="" />', obj.logo.url)
