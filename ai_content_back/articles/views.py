from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer
from .models import Article
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q

# Create your views here.


class ArticleList(APIView):
    """Article list view, that lists all the articles on the database model. Allows only get requests.
     Does not utilize any permission class for this MVP. """

    def get(self, request):
        query = self.request.query_params.get('keyword')
        # print(query)
        if query == None:
            query = ''
        articles = Article.objects.filter(Q(title__icontains=query) | Q(source__icontains=query) | Q(paragraph_one__icontains=query) | Q(paragraph_two__icontains=query))

        page = self.request.query_params.get('page')
        paginator = Paginator(articles, 12)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        
        if page == None:
            page = 1

        page = int(page)

        serializer = ArticleSerializer(articles, many=True)
        return Response({'articles': serializer.data, 'page': page, 'pages': paginator.num_pages})
    

class TopArticle(APIView):
    """Top Article list view, that lists the articles on the database model considering the read_count
    in descending order. Allows only get requests.
     Does not utilize any permission class for this MVP. """

    def get(self, request):
        articles = Article.objects.all().order_by('-read_count').values()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)



class ArticleDetail(APIView):
    """Article detail view gets article detail given an article ID. Allows only GET"""

    # custom method to retrieve article from model given article id.
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get method calls on get_object to retrieve article and return serialized article as response to endpoint 
    # request.
    def get(self, request, id):
        article = self.get_object(id=id)
        article.read_count = article.read_count + 1
        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)