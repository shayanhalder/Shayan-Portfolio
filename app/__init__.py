import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb



mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)
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
