from flask import Flask, render_template

from certifications import db
from certifications.utils import get_syllabus


app = Flask(__name__)
database = db.get()


@app.before_request
def _db_connect():
    database.connect()


@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()


@app.route("/<student_id>")
def main(student_id):
    return render_template('user.j2', syllabus=get_syllabus())
