from http import HTTPStatus

from django.contrib.auth import get_user_model
# from django.test import TestCase
from django.urls import reverse

# from news.models import Comment, News

User = get_user_model()
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


# class TestRoutes(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(title='Заголовок', text='Текст')
#         cls.author = User.objects.create(username='Лев Толстой')
#         cls.reader = User.objects.create(username='Читатель простой')
#         cls.comment = Comment.objects.create(
#             news=cls.news,
#             author=cls.author,
#             text='Текст комментария'
#         )
    
#     def test_availability_for_comment_edit_and_delete(self):
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.reader, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             self.client.force_login(user)
#             for name in ('news:edit', 'news:delete'):  
#                 with self.subTest(user=user, name=name):        
#                     url = reverse(name, args=(self.comment.id,))
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

    
#     def test_redirect_for_anonymous_client(self):
#         login_url = reverse('users:login')
#         for name in ('news:edit', 'news:delete'):
#             with self.subTest(name=name):
#                 url = reverse(name, args=(self.comment.id,))
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)
# import pytest
# from http import HTTPStatus
# from django.urls import reverse
# from pytest_django.asserts import assertRedirects

# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name', 'args'
#     (
#         ('news:home', None),
#         ('users:login',None),
#         ('users:logout', None),
#         ('users:sign',None),
#         ('news:detail', pytest.lazy_fixture('news_id_for_args'))
#     ),
# )
# def test_anon_access_different_pages(client, name, args):
#     url = reverse(name, args=args)
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK

# @pytest.mark.parametrize(
#         'client_parametrized, status'
#         (
#             ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
#             ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
#     ),
# )
# def test_author_access_edit_delete_comment(parametrized_client, name, args, access):
#     url=reverse(name, args=args)
#     response=parametrized_client.get(url)
#     assert response.status_code==access


# @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
#         ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
#     ),
# )
# @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('news:detail', pytest.lazy_fixture('slug_for_args')),
#         ('news:edit', pytest.lazy_fixture('slug_for_args')),
#         ('news:delete', pytest.lazy_fixture('slug_for_args')),
#         ('news:add', None),
#         ('news:success', None),
#         ('news:list', None),
#     ),
# )
# def test_redirects(client, name, args):
#     login_url = reverse('users:login')
#     url = reverse(name, args=args)
#     expected_url = f'{login_url}?next={url}'
#     response = client.get(url)
#     assertRedirects(response, expected_url)




#Новый код:

@pytest.mark.parametrize(
    'page, args',
    (
        (pytest.lazy_fixture('comment_id'),HTTPStatus.OK),
        (pytest.lazy_fixture('comment_id'),HTTPStatus.OK)
    ),
)
def test_pages_availability_for_auth_users(
        page, auth_user, args
):
    url = reverse(page, args=args)
    response = auth_user.get(url)
    assert response.status_code == HTTPStatus 


@pytest.mark.django_db
def test_pages_availability_for_anon_users(
        page, admin_client, args
):
    url = reverse(page, args=args)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus 
    

@pytest.mark.parametrize(
    'page',
    ( 'news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(
        page, news_id, admin_client
):
    url = reverse(page, args=news_id)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus 



@pytest.mark.parametrize(
    'page, args',
    (
        ('news:detail', pytest.lazy_fixture('news_id'),HTTPStatus.OK),
        ('user:login', None),
        ('user:login', None),
        ('user:sign', None),
        ('news:home', None),
    ),
)
def test_redirects(admin_client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = admin_client.get(url)
    assertRedirects(response, expected_url)
