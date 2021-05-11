import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flask_migrate import Migrate
from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10
pagesize = 10
def Categories():
  list_categories = Category.query.all()
  categories = {}
  for category in list_categories:
    categories[category.id] = category.type
  return categories

def getCurrentPage(query,pageno):
  start = (pageno-1)*10
  end = start+10
  count = len([q.id for q in query])
  return query[start:end],count

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
    try:
      categories = Categories()

      return jsonify({
        "success": True,
        "categories": categories
      })

    except:
      abort(422)

  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''



  @app.route('/questions',methods=["GET"])
  def getQuestions():

    page = request.args.get('page',1,type=int)
    questions_query,total_questions = getCurrentPage(db.session.query(Question)\
                                                     .join(Category).all(),page)
    if not questions_query:
      abort(404)

    try:
      questions = [
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
      categories = Categories()

      return jsonify({
        "success":True,
        "total_questions":total_questions,
        "questions":questions,
        "categories": categories,
        "current_category": None
      })

    except:
      abort(422)

  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def deleteQuestion(question_id):

    question = Question.query.filter(Question.id==question_id).one_or_none()
    if not question:
      abort(404)
    try:
      question.delete()
      questions = [question.id for question in Question.query.all()]
      #print (questions)
      return jsonify({
        'success':True,
        'deleted':question_id,
        'total_questions':len(questions)
      })
    except:
      abort(422)

  '''
  @TODO: 
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions',methods=['POST'])
  def createQuestion():

    new_question = request.get_json()
    category = Category.query.get(new_question.get('category_id'))
    if not category:
      abort(404)

    try:
      question = Question(
        question = new_question.get('question'),
        answer = new_question.get('answer'),
        difficulty = new_question.get('difficulty'),
        category = category
      )
      question.insert()
      questions = [question.id for question in Question.query.all()]
      print (question.format())
      return jsonify([{
        'success':True,
        'total_questions':len(questions)
      }])
    except:
      abort(422)

  '''
  @TODO: 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/question',methods=['Post'])
  def questionSearch():
    question = request.get_json()
    term = question.get('term')
    questionFilter = Question.question.ilike(f"%{term}%")
    questions = Question.query.filter(questionFilter).all()
    if not questions:
      abort(404)
    try:
      data = [q.format() for q in questions]
      return jsonify([{
        "success":True,
        "data":data
      }])
    except:
      abort(422)

  '''
  @TODO: 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>',methods=['GET'])
  def getQuestionByCategories(category_id):
    questions = Question.query.filter(Question.category_id==category_id).all()
    if not questions:
      abort(404)
    try:
      category = Category.query.get(category_id)
      category=category.format()
      category['questions']=[
        question.format()
        for question in questions
      ]
      return jsonify([{
          "data":[category],
          "success":True
         }
      ])
    except:
      abort(422)


  '''
  @TODO: 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def playQuiz():
    body = request.get_json()
    prev_questions = body.get("prev_questions")
    category_id = body.get("category_id")

    questions = Question.query.filter(Question.category_id==category_id)\
                        .filter(Question.id.notin_(prev_questions)).all()
    if not questions:
      abort(404)
    try:
      question = random.choice(questions).format()

      return jsonify({
        "success":True,
        "question":question
      })
    except:
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  return app

if __name__ == "__main__":
  app = create_app()
  app.run()