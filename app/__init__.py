import os
import datetime
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

print(os.getenv("MYSQL_DATABASE"))
print(os.getenv("MYSQL_USER"))
print(os.getenv("MYSQL_PASSWORD"))
print(os.getenv("MYSQL_HOST"))

if os.getenv("TESTING") == "true":
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:    
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )
print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb



mydb.connect()
mydb.create_tables([TimelinePost])

# print(mydb)
env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

@app.route('/')
def index():
    return render_template('index.html', title="Shayan Halder", url=os.getenv("URL"))

@app.route('/experience')
def experience():
    template = env.get_template("experience.html")
    return template.render()
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hobbies')
def hobbes():
    template = env.get_template('hobbies.html')
    return template.render()


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    required_fields = {'name', 'content', 'email'}
    invalid_fields = []
    for field in required_fields:
        if field == "email" and ("@" not in request.form[field] and ".com" not in request.form[field]):
            invalid_fields.append(field)
        if field not in request.form or len(request.form[field].strip()) == 0: 
            invalid_fields.append(field)
    
    if invalid_fields:
        message = []
        for field in invalid_fields:
            message.append("Invalid " + field)
        return jsonify({"status_code": 400, "message": message})
    
    name = request.form['name']
    content = request.form['content']
    email = request.form['email']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in 
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/timeline', methods=["GET"])
def timeline():
    return render_template('timeline.html', title='Timeline')
