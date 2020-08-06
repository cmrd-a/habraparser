
from habraparser.celeryapp import app
from .models import Article
from bs4 import BeautifulSoup
from celery import shared_task
import logging
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def parse_habr():
    with open("/mnt/c/habraparser/core/habr.html", "r", encoding="UTF-8") as fp:
        soup = BeautifulSoup(fp, "lxml")

        results = soup.find_all("h2", class_="post__title")

        for i, r in enumerate(results):
            logger.info(f"{i + 1} {r.text.strip()} \n {r.a.get('href')} \n")
