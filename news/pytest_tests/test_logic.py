from http import HTTPStatus
import time

import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse
from news.forms import BAD_WORDS, WARNING

from news.models import Comment, News
from yanews import settings


@pytest.mark.parametrize(
    'parametrized_client, expected_comments_count',
    (
        (lazy_fixture('anon_client'), 0),
        (lazy_fixture('author_client'), 1),
    ),
)
def test_anonymous_user_cant_create_comment(parametrized_client, news, form_data, expected_comments_count):    
    parametrized_client.post(reverse('news:detail', args=(news.id,)), data=form_data)
    assert Comment.objects.count() == expected_comments_count


def test_user_cant_use_bad_words(author_client, news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(reverse('news:detail', args=(news.id,)), data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, news, comment, url_to_comments):
    response = author_client.delete(reverse('news:delete', args=(comment.id,)))
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
    response = not_author_client.delete(reverse('news:delete', args=(comment.id,)))
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, news, comment, url_to_comments, form_data):
    response = author_client.post(reverse('news:edit', args=(comment.id,)), data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']

def test_user_cant_edit_comment_of_another_user(not_author_client, comment, form_data):
    comment_text = comment.text

    response = not_author_client.post(reverse('news:edit', args=(comment.id,)), data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text == comment_text