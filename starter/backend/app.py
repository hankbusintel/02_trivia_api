import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flask_migrate import Migrate
from models import setup_db, Question, Category,db


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

  @app.route('/questions',methods=['POST'])
  def createQuestion():

    new_question = request.get_json()
    category = Category.query.get(new_question.get('category'))
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


  @app.route('/questionSearch',methods=['POST'])
  def questionSearch():
    question = request.get_json()
    term = question.get('searchTerm')
    questionFilter = Question.question.ilike(f"%{term}%")
    questions = Question.query.filter(questionFilter).all()
    total_questions = len(Question.query.all())

    if not questions:
      abort(404)
    try:
      question_data = [q.format() for q in questions]
      print (question_data)
      return jsonify({
        "success":True,
        "questions":question_data,
        "total_questions":total_questions,
        "current_category":None
      })
    except:
      abort(422)


  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def getQuestionByCategories(category_id):
    questions = Question.query.filter(Question.category_id==category_id).all()
    if not questions:
      abort(404)
    try:
      selected_questions = [q.format() for q in questions]
      total_questions = len(Question.query.all())
      return jsonify({
          "success":True,
          "questions":selected_questions,
          "total_questions":total_questions,
          "current_category":None
         }
      )
    except:
      abort(422)

  @app.route('/quizzes',methods=['POST'])
  def playQuiz():
    body = request.get_json()
    prev_questions = body.get("previous_questions")
    quiz_category = body.get("quiz_category")
    if quiz_category['id'] !=0:
      questions = Question.query.filter(Question.category_id==quiz_category['id'])\
                          .filter(Question.id.notin_(prev_questions)).all()
    else:
      questions = Question.query.filter(Question.id.notin_(prev_questions)).all()

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