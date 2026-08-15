from rest_framework import generics

from .models import Announcement, ImportantLink, Member, NewsItem
from .serializers import AnnouncementSerializer, ImportantLinkSerializer, MemberSerializer, NewsItemSerializer


class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class NewsListView(generics.ListAPIView):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer


class NewsDetailView(generics.RetrieveAPIView):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    lookup_field = 'slug'


class MemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ImportantLinkListView(generics.ListAPIView):
    queryset = ImportantLink.objects.all()
    serializer_class = ImportantLinkSerializer
