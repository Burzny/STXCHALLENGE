from rest_framework import serializers
from main.models import Book
from django.core.serializers.json import Serializer


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = (
                    "id",
                    "external_id",
                    "title",
                    "authors",
                    "published_year",
                    "acquired",
                    "thumbnail"
                    )
        
