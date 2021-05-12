## Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2.  **Enviroment** - For all project related python packages and version can be found from requirements.txt file.


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Run the migration script by entering following command in terminal
flask db upgrade

### Running the server


To run the server, in the backend folder execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

API Reference
The Trivia Api is based on REST, returns JSON-encoded responses, and returns standard HTTP response codes.

**Requests**

*1. GET /questions*
Optional Parameter: /questions?page=(1,2,3,...), Return page 1 by default. Each page contains 10 questions.
*Json Response*
{
    "categories": {
    "1": ...
    "2": ...
    },
    "current_category":...,
    "questions": [
        {
        "answer": ...,
        "category": [
            {
            "id": ...,
            "type": ...
            }
        ],
        "difficulty": ...,
        "id": ...,
        "question": ...
        }
    ],
    "success": true,
    "total_questions": ...
}


*2. GET /categories*
Return all available categories.
*Json Response*
{
   "categories": {
   "1": ....,
   "2": ....,
   "3": ....
   },
   "success": true
}

*3. GET /categories/<int:category_id>/questions*
Get all questions base on selected category
*Json Response*
{
    "current_category": ...,
    "questions": [
        {
        "answer":  ...,
        "category": [
            {
            "id":  ...,
            "type":  ...
            }
        ...
        ],
        "difficulty": ...,
        "id":  ...,
        "question":  ...
        }
    ],
    "success": true,
    "total_questions":  ...
}

4. POST /questionSearch
*Payload*
{"searchTerm":...}

*Json Response*
{
    "success":True,
    "questions":[
        {
            "answer":  ...,
            "category": [
                {
                "id":  ...,
                "type":  ...
                }
            ...
            ],
            "difficulty": ...,
            "id":  ...,
            "question":  ...
        }
    ],
    "total_questions":total_questions,
    "current_category":null
}

*5.POST /quizzes*
*Payload*
{
    "previous_questions":[...],
    "quiz_category":{
        "id":...,
        "type":...
    }
}

*Json response*
{
    "question":[
        {
        "answer":  ...,
        "category": [
            {
            "id":  ...,
            "type":  ...
            }
            ...
        ],
        "difficulty": ...,
        "id":  ...,
        "question":  ...
        }
    ]
    "success":True,
}

*6. POST /questions*
*Pay Load*
{
    "category":<category_id>,
    "question":...,
    "answer":...,
    "difficulty":...
}


*Json Response*
{
    'total_questions':...
    'success':True
}

7. DELETE /questions/<int:question_id>
*Json Response*
{
    'success':True,
    'deleted':<question_id>,
    'total_questions':...
}

8. Error Response:
*404 Not found*
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
   
*422 unprocessable*
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}

*400 bad request*
{
    "success": False,
    "error": 400,
    "message": "bad request"
}

*405 metod not allow*
{
    "success": False,
    "error": 405,
    "message": "method not allowed"
}


## Testing
To run the tests, run
```
(1) make a copy of the database for trivia:
CREATE DATABASE trivia_test WITH TEMPLATE trivia

(2) Run the test_flaskr.py script
```
