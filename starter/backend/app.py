import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flask_migrate import Migrate
from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10
pagesize = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  migrate=Migrate(app,db)
  setup_db(app)


  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories',methods=["GET"])
  def getCategories():
    categories = Category.query.all()
    data = [category.format() for category in categories]
    return jsonify(data)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  def getCurrentPage(query,pageno):
    start = (pageno-1)*10
    end = start+10
    count = len([q.id for q in query])
    return query[start:end],count

  @app.route('/questions',methods=["GET"])
  def getQuestions():
    page = request.args.get('page',1,type=int)
    questions_query,total_questions = getCurrentPage(db.session.query(Question)\
                                                     .join(Category).all(),page)
    data = [
      {
        "id":question.id,
        "question":question.question,
        "answer":question.answer,
        "difficulty":question.difficulty,
        "category":[{
          "id":question.category_id,
          "type":question.category.type
        }]
      }
      for question in questions_query
    ]

    return jsonify([{
      "success":True,
      "Total_questions":total_questions,
      "data":data
    }])

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def deleteQuestion(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      questions = [question.format() for question in Question]
      return jsonify({
        'success':True,
        'deleted':question_id,
        'question':questions,
        'total_questions':len(questions)
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  return app

if __name__ == "__main__":
  app = create_app()
  app.run()