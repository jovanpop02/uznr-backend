from rest_framework import serializers

from .models import ImportantLink, Member, NewsImage, NewsItem


class NewsImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsImage
        fields = ['image', 'order']

    def get_image(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class NewsItemSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = NewsItem
        fields = ['slug', 'title', 'excerpt', 'date', 'thumbnail', 'content', 'images']

    def get_thumbnail(self, obj):
        if not obj.thumbnail:
            return None
        request = self.context.get('request')
        url = obj.thumbnail.url
        return request.build_absolute_uri(url) if request else url


class ImportantLinkSerializer(serializers.ModelSerializer):
    href = serializers.SerializerMethodField()
    is_file = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = ImportantLink
        fields = ['title', 'href', 'is_file', 'logo']

    def get_href(self, obj):
        if obj.file:
            request = self.context.get('request')
            url = obj.file.url
            return request.build_absolute_uri(url) if request else url
        return obj.url

    def get_is_file(self, obj):
        return bool(obj.file)

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get('request')
        url = obj.logo.url
        return request.build_absolute_uri(url) if request else url


class MemberSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['name', 'url', 'logo']

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get('request')
        url = obj.logo.url
        return request.build_absolute_uri(url) if request else url
