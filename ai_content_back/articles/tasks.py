import openai
import requests
import os
import dateutil.parser as parser
from bs4 import BeautifulSoup
from .models import Article
from django.http import HttpResponse
from datetime import datetime, timedelta
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY')


@shared_task
def hello():
    logger.info("Hello there!")

# helper function that passes prompt to openai gpt3.5turbo and returns response
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content":prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, )
    return response.choices[0].message["content"]


# helper function to store summarized article in Article model.
def store_article_in_model(article_list):
    # print('store article im model logs')
    # print(len(article_list))
    for article in article_list:
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        current_date = str(current_date)
        current_date = current_date[0:10]
        yesterday = str(yesterday)
        yesterday = yesterday[0:10]
        
        
        try:
            model_article = Article.objects.get(title=article['Title'])
        except:
            model_article = None
        if (current_date == article['Date'] or yesterday == article['Date']) and not model_article:
            try:
                Article.objects.create(
                    title = article['Title'],
                    date = article['Date'],
                    paragraph_one = article['Paragraph_one'],
                    paragraph_two = article['Paragraph_two'],
                    source = article['Source']
                    )
                print('execution')
            except Exception as e:
                print('Something went wrong')
                print(e)
                break
    # return HttpResponse('finished')

# helper function that calls on get_completion(to summarize article using openai's LLM) and calls on
# storearticleinmodel to store the summarized article in Article model.
def summarize_and_store(article_list):
    
    for article in article_list:
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        current_date = str(current_date)
        current_date = current_date[0:10]
        yesterday = str(yesterday)
        yesterday = yesterday[0:10]

        if current_date == article["Date"] or yesterday == article['Date']:
            text = article['Body']


            prompt = f"""
                Summarize the text delimited by triple backticks \
                into 200 words or less.
                The summary should be in two paragraphs.
                ```{text}```
                """
            response = get_completion(prompt)
            response_list = response.split('\n')
            # print(response_list)
            article['Paragraph_one'] = response_list[0]
            article['Paragraph_two'] = response_list[2]
    store_article_in_model(article_list=article_list)


# web scraping function to scrape sciencedaily.com and retrieve articles from AI section.
@shared_task
def sciencedaily_scrapper():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110Safari/537.3'}
    base_url = 'https://www.sciencedaily.com'
    requests_obj = requests.get(base_url + '/news/computers_math/artificial_intelligence/',headers=headers, verify=False)
    soup_obj = BeautifulSoup(requests_obj.content, 'html.parser')
    a_tags = soup_obj.find_all("a")


    releases_list = []
    for tags in a_tags:
        if 'releases' in tags['href']:
            releases_list.append(tags['href'])


    article_list=[]
    for articles_link in releases_list[0:5]:
        content_url = base_url + articles_link
        requests_article_obj = requests.get(content_url, headers=headers)
        soup_article_obj = BeautifulSoup(requests_article_obj.content, 'html.parser')


        for span in soup_article_obj(['span']):
            span.decompose()

        introduction = soup_article_obj.find("p", id = "first").text

        title = soup_article_obj.find("h1", id = "headline").text.strip()

        date = soup_article_obj.find("dd", id = "date_posted").text.strip()
        date = parser.parse(date)
        date = date.isoformat()
        date = date[0:10]

        source = soup_article_obj.find('dd', id = "source").text.strip()

        content = soup_article_obj.find("div", id = "text")
        content = content.text.strip()
        content = " ".join(content.split())

        articles_dict = {}
        articles_dict['Title'] = title
        articles_dict['Date'] = date
        articles_dict['Source'] = source
        articles_dict['Body'] = introduction + content
        articles_dict['Paragraph_one'] = ''
        articles_dict['Paragraph_two'] = ''
        article_list.append(articles_dict)
    # print('scrapper function log')
    # print(len(article_list))
    summarize_and_store(article_list)
    # return HttpResponse('doneeee')


# web scraping function to scrape venturebeat.com and retrieve articles from AI section.
@shared_task
def venturebeat_scrapper():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110Safari/537.3'}
    base_url = 'https://venturebeat.com/category/ai/'
    requests_obj = requests.get(base_url ,headers=headers, verify=False)
    soup_obj = BeautifulSoup(requests_obj.content, 'html.parser')
    a_tags = soup_obj.find_all("a")


    releases_list = []
    for tags in a_tags[62:]:
        releases_list.append(tags['href'])


    article_list=[]
    for articles_link in releases_list[0:5]:
        # content_url = base_url + articles_link
        requests_article_obj = requests.get(articles_link, headers=headers)
        soup_article_obj = BeautifulSoup(requests_article_obj.content, 'html.parser')



        # introduction = soup_article_obj.find("p", id = "first").text

        title = soup_article_obj.find("h1", {'class': 'article-title'}).text.strip()

        date = soup_article_obj.find("time", {'class': 'the-time'}).text.strip()
        date = parser.parse(date)
        date = date.isoformat()
        date = date[0:10]

        source = soup_article_obj.find('div', {'class': 'Article__author-info'}).text.strip()

        content = soup_article_obj.find("div", {'class': 'article-content'})
        content = content.find_all('p',)
        full_content = ''
        for p in content[1:-6]:
            full_content += p.text

        articles_dict = {}
        articles_dict['Title'] = title
        articles_dict['Date'] = date
        articles_dict['Source'] = source
        articles_dict['Body'] = full_content
        article_list.append(articles_dict)
    # print('scrapper function log')
    # print(len(article_list))
    summarize_and_store(article_list)
    # return HttpResponse('doneeee')


# web scraping function to scrape uniteai.com.
@shared_task
def uniteai_scrapper():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110Safari/537.3'}
    base_url = 'https://www.unite.ai/'
    requests_obj = requests.get(base_url ,headers=headers, verify=False)
    soup_obj = BeautifulSoup(requests_obj.content, 'html.parser')
    a_tags = soup_obj.find_all("a")


    releases_list = []
    for tags in a_tags[123:]:
        releases_list.append(tags['href'])


    article_list=[]
    for articles_link in releases_list[0:5]:
        # content_url = base_url + articles_link
        requests_article_obj = requests.get(articles_link, headers=headers)
        soup_article_obj = BeautifulSoup(requests_article_obj.content, 'html.parser')



        # introduction = soup_article_obj.find("p", id = "first").text

        title = soup_article_obj.find("h1", {'class': 'mvp-post-title left entry-title'}).text.strip()

        date = soup_article_obj.find("div", {'class': 'mvp-author-info-date left relative'})
        date = date.find('meta')['content']
        date = parser.parse(date)
        date = date.isoformat()
        date = date[0:10]

        source = soup_article_obj.find('div', {'class': 'mvp-author-info-name left relative'})
        source = source.find('a').text.strip()

        content = soup_article_obj.find_all('p',)
        full_content = ''
        for p in content[3:-10]:
            full_content += p.text

        articles_dict = {}
        articles_dict['Title'] = title
        articles_dict['Date'] = date
        articles_dict['Source'] = source
        articles_dict['Body'] = full_content
        article_list.append(articles_dict)
    # print('scrapper function log')
    # print(len(article_list))
    summarize_and_store(article_list)
    # return HttpResponse('doneeee')