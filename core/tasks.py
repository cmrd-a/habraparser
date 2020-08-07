from contextlib import closing

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Article

logger = get_task_logger(__name__)


def parse_posts_urls(soup):
    """Сформировать список ссылок на посты.

    Args:
        soup  (BeautifulSoup): страница, содержащуя список постов Хабра
    """
    links = soup.find_all("h2", class_="post__title")
    urls = []
    for link in links:
        urls.append(link.a.get("href"))
    return urls


def make_soup(url):
    """Получить html-страницу по url.

    Args:
        url (str): адрес ведущий на html-страницу
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            content_type = resp.headers["Content-Type"].lower()
            if (
                    resp.status_code == 200
                    and content_type is not None
                    and content_type.find("html") > -1
            ):
                return BeautifulSoup(resp.content, "html.parser")
            else:
                return None

    except requests.RequestException as e:
        logger.error(f"Error during requests to {url} : {str(e)}")
        return None


@shared_task
def parse_daily():
    """ Парсинг и сохранение лучших за день статей Хабра.

    После парсинга главной страницы формируются ссылки на посты на этой странице и ссылки на отстальные страницы.
    Парсинг отсальных страниц дополняет список ссылок на посты.
    Затем выполняется пасинг каждого поста и его сохранение в БД.
    """
    soup = make_soup("http://habr.com/ru/")

    posts_urls = parse_posts_urls(soup)

    for page_button in soup.find_all(class_="toggle-menu__item-link_pagination"):
        if page_button.attrs.get("href", None):
            page_url = "https://habr.com" + page_button.attrs.get("href")
            posts_urls.extend(parse_posts_urls(make_soup(page_url)))

    for url in posts_urls:
        try:
            parse_post.delay(url)
        except parse_post.OperationalError as e:
            logger.exception(f"Sending task raised: {e}")


@shared_task
def parse_post(post_url):
    """Парсинг и сохранение поста.

    Выполняется проверка наличия поста в БД по url.
    Из полученной по url странице берётся заголовок и тело статьи.
    Данные сохраняюся в БД путём создания объекта.

    Args:
        post_url (str): ссылка на пост Хабра
    """
    try:
        existed = Article.objects.get(url=post_url)
    except Article.DoesNotExist:
        existed = None

    if not existed:
        soup = make_soup(post_url)
        try:
            title = soup.find("h1", class_="post__title_full").text.strip()
            body = soup.find("div", class_="post__text").text.strip()
        except AttributeError:
            logger.error(f"{post_url} parsing error")
            return
        Article.objects.create(url=post_url, title=title, body=body)
        logger.info(f"{post_url} successfuly saved")
    else:
        logger.warning(f"{post_url} is already existed")
