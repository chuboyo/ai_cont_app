from django.urls import path
from .views import ArticleList, ArticleDetail, TopArticle
from .tasks import sciencedaily_scrapper, venturebeat_scrapper, uniteai_scrapper

# endpoints for articles
urlpatterns = [
    path('articles/', ArticleList.as_view(), name='articles'),
    path('toparticles/', TopArticle.as_view(), name='toparticles'),
    path('articles/<int:id>/', ArticleDetail.as_view(), name='articles-detail'),
    # path('sciencedaily_scrape/', sciencedaily_scrapper),
    # path('venturebeat_scrape/', venturebeat_scrapper),
    # path('uniteai_scrape/', uniteai_scrapper),
]