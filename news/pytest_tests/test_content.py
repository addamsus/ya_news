from http import HTTPStatus
import time

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

from news.models import Comment, News
from yanews import settings


def test_news_count_on_homepage(anon_client, all_news):
    response = anon_client.get(reverse('news:home'))
    object_list = response.context['object_list']
    
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE

def test_news_order_on_homepage(anon_client, all_news):
    response = anon_client.get(reverse('news:home'))
    object_list = response.context['object_list']
    
    for i in range(len(object_list) - 1):
        assert object_list[i].date > object_list[i+1].date

def test_comments_order(author_client, author, news):
    for i in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='cccc',
        )
        time.sleep(0.2)

    response = author_client.get(reverse('news:detail', args=(news.pk,)))
    comment_list = response.context['news'].comment_set.all()
    
    for i in range(len(comment_list) - 1):
        assert comment_list[i].created < comment_list[i+1].created


@pytest.mark.parametrize(
    'parametrized_client, has_form',
    (
        (lazy_fixture('anon_client'), False),
        (lazy_fixture('author_client'), True),
    ),
)
def test_form_access_anon(parametrized_client, has_form, news):
    response = parametrized_client.get(reverse('news:detail', args=(news.pk,)))
    assert ('form' in response.context) == has_form
