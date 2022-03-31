import datetime
from operator import truediv
from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone
from .models import Question

# Models y Vistas
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for Questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor Course Director de Platzi? Futuro",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False) #assertEqual

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for Questions whose pub_date is in the past a long ago"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="¿Quien es el mejor Course Director de Platzi? Pasado",pub_date=time)
        self.assertIs(past_question.was_published_recently(), False) #assertEqual  

    def test_was_published_recently_with_recent_questions(self):
        """was_published_recently returns False for Questions whose pub_date recently"""
        time = timezone.now() - datetime.timedelta(days=1)
        recently_question = Question(question_text="¿Quien es el mejor Course Director de Platzi? Presente",pub_date=time)
        self.assertIs(recently_question.was_published_recently(), True) #assertEqual       

    def test_was_published_recently_with_now_questions(self):
        """was_published_recently returns False for Questions whose pub_date recently"""
        time = timezone.now()
        now_question = Question(question_text="¿Quien es el mejor Course Director de Platzi? Presente",pub_date=time)
        self.assertIs(now_question.was_published_recently(), True) #assertEqual    

def create_question(question_text, days):
    """
    Create a question with the given "question text", and published the given
    number of days offset to now (negative for questions published in the past,
    positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))   
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")   
        self.assertQuerysetEqual(response.context["latest_question_list"], [])   

    def test_future_question(self):
        """
        Question with a pub_date in the future aren't displayed on the index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Past question", days=30)   
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],[past_question]
        ) 

    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],[past_question1, past_question2]
        ) 

    def test_two_future_questions(self):
        """The questions index page may display multiple questions"""
        create_question("Future question 1", days=30)
        create_question("Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context["latest_question_list"],[]
        )         

class QuestionDetailViewTests(TestCase):
    def test_future_questions(self):
        """
        The detail view of a question with a pub_date in the future 
        returns a 404 error not found
        """
        future_question = create_question(question_text="Past question", days=30)  
        url = reverse("polls:detail", args=(future_question.id,)) #id == pk 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-30)  
        url = reverse("polls:detail", args=(past_question.id,)) #id == pk 
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)        

# Test results views (Curso Intermedio Django '8')

# Questions sin choices (Curso Intermedio Django '8')