import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path =  "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question={
            "question":"What is the name of the highest mountain in the world?",
            "answer":"everest",
            "difficulty":1,
            "category":1
        }
        self.quizz = {
            "previous_questions":[21], "quiz_category": {"type": "Science", "id": 1}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getPaginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'],True)
        self.assertTrue(len(data['questions']))

    def test_404_forquestion_page_outofrange(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data["categories"]))

    def test_404_question_delete(self):
        res = self.client().delete('/questions/50000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_question_deletion(self):
        question = Question.query.filter(Question.question==self.new_question['question']).one_or_none()
        #print (question.format()['id'])
        res = self.client().delete('/questions/'+str(question.id))
        data = json.loads(res.data)

        question_delete = Question.query.filter(Question.id==question.id).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],question.id)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question_delete,None)

    def test_create_question(self):
        res = self.client().post('/questions',json=self.new_question)
        question = Question.query.filter(Question.question==self.new_question['question'])

        self.assertEqual(res.status_code,200)
        self.assertIsNotNone(question)

    def test_404_create_question(self):
        new_question = self.new_question
        new_question['category']=5000
        res = self.client().post('/questions',json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_question_search(self):
        res = self.client().post('/questionSearch',json={"searchTerm":"clay"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_question_search(self):
        res = self.client().post('/questionSearch',json={"search":"asjidaijsidj"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'],True)
        self.assertTrue(len(data['questions']))

    def test_404_question_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_play_quiz(self):
        res = self.client().post('/quizzes',json=self.quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data['question']),True)

    def test_404_play_quiz(self):
        quizz=self.quizz
        quizz['quiz_category']['id']=1000
        quizz['quiz_category']['type']='unknown'
        res = self.client().post('/quizzes',json=quizz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()