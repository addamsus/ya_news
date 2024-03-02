# conftest.py
from datetime import datetime
from django.urls import reverse
import pytest

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель новости, чтобы создать экземпляр.
from news.models import Comment, News
from yanews import settings


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client

@pytest.fixture
def anon_client(author):
    client = Client()
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='pepeska',
        created=datetime(2001, 1, 1),
    )
    return comment


@pytest.fixture
def another_comment(news, django_user_model):
    comment = Comment.objects.create(
        news=news,
        author=django_user_model.objects.create(username='Авторка'),
        text='pepeska 2',
    )
    return comment

@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@pytest.fixture
def all_news():
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE * 2):
        news = News(
            title=f'Новость {index}',
            text='Просто kek.',
            date=datetime(year=2000+index, month=1, day=1)
        )
        all_news.append(news)
    News.objects.bulk_create(all_news)

    return all_news


@pytest.fixture
def url_to_comments(news):
    return reverse('news:detail', args=(news.id,)) + '#comments'
