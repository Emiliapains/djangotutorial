import datetime

from django.db import transaction
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase
from django.urls import reverse, resolve
from django.utils import timezone
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from .models import Question
from .views import IndexView


# class QuestionModelTests(TestCase):
#     #From Tutorial
#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
#
#         def create_question(question_text, days):
#             """
#             Create a question with the given `question_text` and published the
#             given number of `days` offset to now (negative for questions published
#             in the past, positive for questions that have yet to be published).
#             """
#             time = timezone.now() + datetime.timedelta(days=days)
#             return Question.objects.create(question_text=question_text, pub_date=time)
#
#         class QuestionDetailViewTests(TestCase):
#             def test_future_question(self):
#                 """
#                 The detail view of a question with a pub_date in the future
#                 returns a 404 not found.
#                 """
#                 future_question = create_question(question_text="Future question.", days=5)
#                 url = reverse("polls:detail", args=(future_question.id,))
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, 404)
#
#             def test_past_question(self):
#                 """
#                 The detail view of a question with a pub_date in the past
#                 displays the question's text.
#                 """
#                 past_question = create_question(question_text="Past Question.", days=-5)
#                 url = reverse("polls:detail", args=(past_question.id,))
#                 response = self.client.get(url)
#                 self.assertContains(response, past_question.question_text)
#         class QuestionIndexViewTests(TestCase):
#             def test_no_questions(self):
#                 """
#                 If no questions exist, an appropriate message is displayed.
#                 """
#                 response = self.client.get(reverse("polls:index"))
#                 self.assertEqual(response.status_code, 200)
#                 self.assertContains(response, "No polls are available.")
#                 self.assertQuerySetEqual(response.context["latest_question_list"], [])
#
#             def test_past_question(self):
#                 """
#                 Questions with a pub_date in the past are displayed on the
#                 index page.
#                 """
#                 question = create_question(question_text="Past question.", days=-30)
#                 response = self.client.get(reverse("polls:index"))
#                 self.assertQuerySetEqual(
#                     response.context["latest_question_list"],
#                     [question],
#                 )
#
#             def test_future_question(self):
#                 """
#                 Questions with a pub_date in the future aren't displayed on
#                 the index page.
#                 """
#                 create_question(question_text="Future question.", days=30)
#                 response = self.client.get(reverse("polls:index"))
#                 self.assertContains(response, "No polls are available.")
#                 self.assertQuerySetEqual(response.context["latest_question_list"], [])
#
#             def test_future_question_and_past_question(self):
#                 """
#                 Even if both past and future questions exist, only past questions
#                 are displayed.
#                 """
#                 question = create_question(question_text="Past question.", days=-30)
#                 create_question(question_text="Future question.", days=30)
#                 response = self.client.get(reverse("polls:index"))
#                 self.assertQuerySetEqual(
#                     response.context["latest_question_list"],
#                     [question],
#                 )
#
#             def test_two_past_questions(self):
#                 """
#                 The questions index page may display multiple questions.
#                 """
#                 question1 = create_question(question_text="Past question 1.", days=-30)
#                 question2 = create_question(question_text="Past question 2.", days=-5)
#                 response = self.client.get(reverse("polls:index"))
#                 self.assertQuerySetEqual(
#                     response.context["latest_question_list"],
#                     [question2, question1],
#                 )
 #From Lab5
class PollsURLTest(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('polls:index')
        self.assertEqual(resolve(url).func.__name__, IndexView.as_view().__name__)

class AssertEquals(TestCase):
    def numberTest(self):
        number = 10
        self.assertEqual(number, 10)

class QuestionModelTest(TestCase):
    def test_str_representation(self):
        question = Question(question_text="What's new?", pub_date=timezone.now())
        self.assertEqual(str(question), question.question_text)

class PollsTransactionTest(TransactionTestCase):
    def test_transaction_rollback(self):
        with self.assertRaises(Exception):
            with transaction.atomic():
                Question.objects.create(question_text="Test question", pub_date=timezone.now())
                self.assertEqual(Question.objects.count(), 1)
                raise Exception("Force rollback")
        self.assertEqual(Question.objects.count(), 0)

class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/admin/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("myuser")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("secret")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()