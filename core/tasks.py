from habraparser.celeryapp import app
from .models import Article
from bs4 import BeautifulSoup
from celery import shared_task
import logging
from contextlib import closing
import requests

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def make_soup(url):
    try:
        page = requests.get(url)
    except requests.RequestException as e:
        logger.error(f"{url} request error {str(e)}")
    return BeautifulSoup(page.content, "lxml")


def parse_posts_urls(soup):
    links = soup.find_all("h2", class_="post__title")
    urls = []
    for link in links:
        urls.append(link.a.get('href'))
    return urls


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except requests.RequestException as e:
        logger.error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


@shared_task
def parse_daily():
    first_soup = make_soup("http://habr.com/ru/")
    posts_urls = parse_posts_urls(first_soup)

    for page_button in first_soup.find_all(class_="toggle-menu__item-link_pagination"):
        if page_button.attrs.get("href", None):
            page_url = "https://habr.com" + page_button.attrs.get('href')
            posts_urls.extend(parse_posts_urls(make_soup(page_url)))

    for i, url in enumerate(posts_urls):
        parse_post.delay(url)
        logger.info(f"{i} {url}")


@shared_task
def parse_post(post_url):
    article, created = Article.objects.get_or_create(url=post_url)
    if created:
        soup = BeautifulSoup(simple_get(post_url), "html.parser")
        try:
            title = soup.find(class_="post__title_full").text
        except AttributeError:
            # article.delete()
            return

        body = soup.find("div", class_="post__text").text
        article.title = title
        article.body = body
        article.save()
        logger.info(f"{post_url} successfuly saved")
    else:
        logger.warning(f"{post_url} is already existed")
