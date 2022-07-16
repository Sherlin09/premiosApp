import datetime
from urllib import response

from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase


from polls.models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿cual es el mejor course director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
     time = timezone.now() + datetime.timedelta(days=days)
     return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        """if no question exist , an aporpiate message is displayed"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], []) 

    def test_future_question(self):
        """ No public questions del future """
        create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_past_question(self):
        """ Question with a pub_date in the past are displayed on the index page """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_future_question_and_past_question(self):
        """ Even if both past and future question exist, only past questions are displayed """
        past_question = create_question(question_text="past question", days=-30)
        future_question = create_question(question_text="future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuersetEqual(
            response.context["latest_question_list"],
            [past_question]
        )


    def test_two_past_questions(self):
        """ The questions index page may display multiple questions """
        past_question1 = create_question(question_text="past question 1", days=-30)
        past_question2 = create_question(question_text="past question 2", days=-60)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        ) 


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="future question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text) 