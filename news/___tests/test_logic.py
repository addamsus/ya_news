# # news/tests/test_logic.py
from http import HTTPStatus
from random import choice
import pytest
from pytest_django.asserts import assertFormError, assertRedirects
from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
from django.urls import reverse


from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.forms import WARNING

User = get_user_model()


# class TestCommentCreation(TestCase):
#     COMMENT_TEXT = 'Текст комментария'

#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(title='Заголовок', text='Текст')
#         cls.url = reverse('news:detail', args=(cls.news.id,))
#         cls.user = User.objects.create(username='Мимо Крокодил')
#         cls.auth_client = Client()
#         cls.auth_client.force_login(cls.user)
#         cls.form_data = {'text': cls.COMMENT_TEXT}

#     def test_anonymous_user_cant_create_comment(self):    
#         self.client.post(self.url, data=self.form_data)
#         comments_count = Comment.objects.count()
#         self.assertEqual(comments_count, 0)
    
#     def test_user_can_create_comment(self):
#         response = self.auth_client.post(self.url, data=self.form_data)
#         self.assertRedirects(response, f'{self.url}#comments')
#         comments_count = Comment.objects.count()
#         self.assertEqual(comments_count, 1)
#         comment = Comment.objects.get()
#         self.assertEqual(comment.text, self.COMMENT_TEXT)
#         self.assertEqual(comment.news, self.news)
#         self.assertEqual(comment.author, self.user)
    
#     def test_user_cant_use_bad_words(self):
#         bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
#         response = self.auth_client.post(self.url, data=bad_words_data)
#         self.assertFormError(
#             response,
#             form='form',
#             field='text',
#             errors=WARNING
#         )
#         comments_count = Comment.objects.count()
#         self.assertEqual(comments_count, 0)

# class TestCommentEditDelete(TestCase):
#     COMMENT_TEXT = 'Текст комментария'
#     NEW_COMMENT_TEXT = 'Обновлённый комментарий'

#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(title='Заголовок', text='Текст')
#         news_url = reverse('news:detail', args=(cls.news.id,))  # Адрес новости.
#         cls.author = User.objects.create(username='Автор комментария')
#         cls.author_client = Client()
#         cls.author_client.force_login(cls.author)
#         cls.reader = User.objects.create(username='Читатель')
#         cls.reader_client = Client()
#         cls.reader_client.force_login(cls.reader)
#         cls.comment = Comment.objects.create(
#             news=cls.news,
#             author=cls.author,
#             text=cls.COMMENT_TEXT
#         )
#         cls.edit_url = reverse('news:edit', args=(cls.comment.id,))
#         cls.delete_url = reverse('news:delete', args=(cls.comment.id,))
#         cls.form_data = {'text': cls.NEW_COMMENT_TEXT}
    
#     def test_author_can_delete_comment(self):
#         response = self.author_client.delete(self.delete_url)
#         self.assertRedirects(response, self.url_to_comments)
#         comments_count = Comment.objects.count()
#         self.assertEqual(comments_count, 0)
    
#     def test_user_cant_delete_comment_of_another_user(self):
#         response = self.reader_client.delete(self.delete_url)
#         self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
#         comments_count = Comment.objects.count()
#         self.assertEqual(comments_count, 1)
    
#     def test_author_can_edit_comment(self):
#         response = self.author_client.post(self.edit_url, data=self.form_data)
#         self.assertRedirects(response, self.url_to_comments)
#         self.comment.refresh_from_db()
#         self.assertEqual(self.comment.text, self.NEW_COMMENT_TEXT)

#     def test_user_cant_edit_comment_of_another_user(self):
#         response = self.reader_client.post(self.edit_url, data=self.form_data)
#         self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
#         self.comment.refresh_from_db()
#         self.assertEqual(self.comment.text, self.COMMENT_TEXT)




#PYTEST VERSION


# def test_user_can_create_comment(author_client, author, news, form_data):
#     url = reverse('comment:add')
#     response = author_client.post(url, data=form_data)
#     assertRedirects(response, reverse('notes:success'))
#     assert Comment.objects.count() == 1
#     new_comment = Comment.objects.get()
#     assert new_comment.text == form_data['text']
#     assert new_comment.news == form_data['news']
#     assert new_comment.author == author

def test_user_can_create_comment(author_client, author, form_data, news):#вроде готово
    url = reverse('news:add', args=[news.pk])
    expected_len=Comment.objects.count()+1
    response = author.post(url, data=form_data)
    assertRedirects(response, reverse('news:success'))
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert expected_len == expected_len
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author_client


@pytest.mark.django_db
def test_anonymous_cant_create_comment(client, form_data, comment_id):#вроде готово
    url = reverse('news:add',args=comment_id)
    # response = client.post(url, data=form_data)
    # login_url = reverse('users:login')
    expected_count=Comment.objects.count()
    client.post(url, data=form_data)
    comment_count=Comment.objects.count()
    assert expected_count == comment_count


@pytest.mark.django_db 

def test_bad_words_ban(author_client, comment_data_form, news_url_detailed):
    expected_result = Comment.objects.count()
    comment_data_form['text'] = f'Текст, {choice(BAD_WORDS)}, текст.'
    response = author_client.post(
        news_url_detailed, data=comment_data_form
    )
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == expected_result



#ГОТОВО BY AUTHOR
# def test_author_can_edit_comment(comment, author_client, comment_edit_url, comment_data_form, news_url_detailed):
#     news_url = news_url_detailed+'#comments'
#     authors_news=comment.news
#     author_original=comment.author
#     comment_data_form['text']='Новый такст'
#     responce=author_client.post(comment_edit_url, comment_data_form)
#     assertRedirects(responce, news_url)
#     comment.refresh_from_db()
#     news_edited=comment.mews
#     assert responce.status_code == HTTPStatus.FOUND
#     assert authors_news==news_edited
#     assert comment.text == comment_data_form['text']
#     assert author_original==comment.author

def test_author_can_edit_comment(author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.slug,))
    response = author_client.post(url, form_data)
    assertRedirects(response, reverse('news:success'))
    comment.refresh_from_db()
    assert comment.title == form_data['title']
    assert comment.text == form_data['text']
    assert comment.slug == form_data['slug']
# def test_author_can_delete_comment(author_client,comment_url_deleted, news_url_detailed):
#     result = Comment.objects.count() - 1
#     comments_url = news_url_detailed + '#comments'
#     response = author_client.delete(comment_url_deleted)
#     assertRedirects(response, comments_url)
#     assert response.status_code == HTTPStatus.FOUND
#     assert Comment.objects.count() == result

def test_author_can_delete_comment(author_client, slug_for_args):
    url = reverse('news:delete', args=slug_for_args)
    response = author_client.post(url)
    assertRedirects(response, reverse('news:success'))
    assert Comment.objects.count() == 0

# #OTHER USERS + COMMENTS
# def test_other_user_cant_edit_comment(comment_url_edited, admin_client, comment_data_form, author,comment ):
#     # url = reverse('notes:edit', args=(note.slug,))
#     response = admin_client.post(comment_data_form, comment_url_edited)
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     comment.refresh_from_db()
#     assert comment.author == author
#     assert comment.text == comment_data_form['text']

def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.slug,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Comment.objects.get(id=comment.id)
    assert comment.title == note_from_db.title
    assert comment.text == note_from_db.text
    assert comment.slug == note_from_db.slug

# def test_other_user_cant_delete_comment(comment_delete_url, admin_client):#ГОТОВО
#     expected_result = Comment.objects.count()
#     response = admin_client.delete(comment_delete_url)
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert Comment.objects.count() == expected_result

def test_other_user_cant_delete_comment(not_author_client, form_data, slug_for_args):
    url = reverse('news:delete', args=slug_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1