from rest_framework import serializers 
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    '''Article serializer to serialize article model fields into JSON format. 
    Inherits from serializers.ModelSerializers'''

    class Meta:
        model = Article
        fields = '__all__'