# test_routes.py
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

from news.models import News


@pytest.mark.parametrize(
    'parametrized_client, name, expected_status',
    (
        (lazy_fixture('anon_client'), 'news:home', HTTPStatus.OK),
        (lazy_fixture('anon_client'), 'users:login', HTTPStatus.OK),
        (lazy_fixture('anon_client'), 'users:logout', HTTPStatus.OK),
        (lazy_fixture('anon_client'), 'users:signup', HTTPStatus.OK),
    ),
)
def test_pages_availability(
    parametrized_client, expected_status, name,
):
    url = reverse(name)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status 


@pytest.mark.parametrize(
    'parametrized_client, name, expected_status',
    (
        (lazy_fixture('anon_client'), 'news:detail', HTTPStatus.OK),
    ),
)
def test_pages_availability2(
    parametrized_client, expected_status, name, news
):
    url = reverse(name, args=(news.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'parametrized_comment, expected_status',
    (
        (lazy_fixture('comment'), HTTPStatus.OK),
        (lazy_fixture('another_comment'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_comments_availability(
    author_client, name, parametrized_comment, expected_status
):
    url = reverse(name, args=(parametrized_comment.pk,))
    response = author_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_comments_anon_redirect(
    anon_client, name, comment
):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.pk,))
    expected_url = f'{login_url}?next={url}'
    response = anon_client.get(url)
    assertRedirects(response, expected_url)
