# # news/tests/test_content.py
from django.conf import settings
# from django.test import TestCase
# from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
# from django.utils import timezone

from news.models import Comment, News
from news.forms import CommentForm, NewsForm

User = get_user_model()
START_URL=reverse('news:home')
LEN_NEWS_START_PAGE=10

# class TestHomePage(TestCase):
#     HOME_URL = reverse('news:home')

#     @classmethod
#     def setUpTestData(cls):
#         # Вычисляем текущую дату.
#         today = datetime.today()
#         all_news = [
#             News(
#                 title=f'Новость {index}',
#                 text='Просто текст.',
#                 # Для каждой новости уменьшаем дату на index дней от today,
#                 # где index - счётчик цикла.
#                 date=today - timedelta(days=index)
#             )
#             for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
#         ]
#         News.objects.bulk_create(all_news) 

#     def test_news_count(self):
#         response = self.client.get(self.HOME_URL)
#         object_list = response.context['object_list']
#         news_count = object_list.count()
#         self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)


# class TestDetailPage(TestCase):
#     HOME_URL = reverse('news:home')

#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(
#             title='Тестовая новость', text='Просто текст.'
#         )
#         # Сохраняем в переменную адрес страницы с новостью:
#         cls.detail_url = reverse('news:detail', args=(cls.news.id,))
#         cls.author = User.objects.create(username='Комментатор')
#         # Запоминаем текущее время:
#         # now = datetime.now()
#         now = timezone.now()
#         # Создаём комментарии в цикле.
#         for index in range(10):
#             # Создаём объект и записываем его в переменную.
#             comment = Comment.objects.create(
#                 news=cls.news, author=cls.author, text=f'Tекст {index}',
#             )
#             # Сразу после создания меняем время создания комментария.
#             comment.created = now + timedelta(days=index)
#             # И сохраняем эти изменения.
#             comment.save() 

#     def test_news_order(self):
#         response = self.client.get(self.HOME_URL)
#         object_list = response.context['news_feed']
#         all_dates = [news.date for news in object_list]
#         sorted_dates = sorted(all_dates, reverse=True)
#         self.assertEqual(all_dates, sorted_dates)


#     def test_comments_order(self):
#         response = self.client.get(self.detail_url)
#         # Проверяем, что объект новости находится в словаре контекста
#         # под ожидаемым именем - названием модели.
#         self.assertIn('news', response.context)
#         # Получаем объект новости.
#         news = response.context['news']
#         # Получаем все комментарии к новости.
#         all_comments = news.comment_set.all()
#         # Собираем временные метки всех новостей.
#         all_timestamps = [comment.created for comment in all_comments]
#         # Сортируем временные метки, менять порядок сортировки не надо.
#         sorted_timestamps = sorted(all_timestamps)
#         # Проверяем, что id первого комментария меньше id второго.
#         self.assertEqual(all_timestamps, sorted_timestamps)
    
#     def test_anonymous_client_has_no_form(self):
#         response = self.client.get(self.detail_url)
#         self.assertNotIn('form', response.context)
        
#     def test_authorized_client_has_form(self):
#         # Авторизуем клиент при помощи ранее созданного пользователя.
#         self.client.force_login(self.author)
#         response = self.client.get(self.detail_url)
#         self.assertIn('form', response.context)
#         # Проверим, что объект формы соответствует нужному классу формы.
#         self.assertIsInstance(response.context['form'], CommentForm)
import pytest

@pytest.mark.django_db(
        # 'parametrized_client, news_in_list',
        # (
        #     (pytest.lazy_fixture('author_client'), True),
        #     (pytest.lazy_fixture('not_author_client'), False),
        # )
    )
def test_len_news(client, news_in_list):
    client.get(START_URL)
    len_news=News.oblects.count()
    assert len_news==settings.LEN_NEWS_START_PAGE
    # url = reverse('news:list')
    # response = parametrized_client.get(url)
    # object_list = response.context['object_list']
    # assert (news in object_list) is news_in_list

def test_soert_news(client, news_in_list):
    response=client.get(START_URL)
    news_list=response.context['news_list']
    all_news=[news.date for news in news_list]
    sorted_news= sorted(all_news, reverse=True)
    assert all_news==sorted_news


def test_sort_comments(client, comment_data, comment_url):
    response=client.get(comment_url)
    news=response.context['news']
    comments= news.comment_set.all()
    created_dates=[comment. created for comments]
    sorted_created_dates=sorted(created_dates)
    assert created_dates==sorted_created_dates





# def test_create_news_page_contains_form(author_client):
#     url = reverse('news:add')
#     response = author_client.get(url)
#     assert 'form' in response.context
#     assert isinstance(response.context['form'], CommentForm)

# def test_edit_news_page_contains_form(slug_for_args, author_client):
#     url = reverse('news:edit', args=slug_for_args)
#     response = author_client.get(url)
#     assert 'form' in response.context
#     assert isinstance(response.context['form'], CommentForm)









#юзер создает комментарии
@pytest.mark.parametrize(
        'name, args',
        (
            ('news:add', None),
            ('news:edit', pytest.lazy_fixture('slug_for_args'))
        )
    )


# @pytest.mark.django_db
@pytest.mark.parametrize(
        'parametrized_client, news_in_list',
        (
            (pytest.lazy_fixture('author_client'), True),
            (pytest.lazy_fixture('not_author_client'), False),
        )
    )

def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)