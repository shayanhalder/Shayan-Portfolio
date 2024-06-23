import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape

load_dotenv()
app = Flask(__name__)


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
    return template.render(experience_title="Major League Hacking", date_range="January 2024 - Present", 
                            role_name="SWE Intern", location="Remote", content="Learned about Production Engineering")

