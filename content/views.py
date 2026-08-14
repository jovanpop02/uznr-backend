from rest_framework import generics

from .models import ImportantLink, Member, NewsItem
from .serializers import ImportantLinkSerializer, MemberSerializer, NewsItemSerializer


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
