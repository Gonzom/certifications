from flask import Flask, abort, render_template
from http import HTTPStatus


from certifications import db
from certifications.config import STATIC_PATH
from certifications.generator import get_certification_url
from certifications.utils import get_syllabus


app = Flask(__name__, static_folder=str(STATIC_PATH))
database = db.get()


@app.before_request
def _db_connect() -> None:
    database.connect()


@app.teardown_request
def _db_close(exc) -> None:
    if not database.is_closed():
        database.close()


@app.route("/<student_id>")
def main(student_id: str) -> str:
    user = db.User.get_or_none(url=student_id)
    if not user:
        return abort(HTTPStatus.NOT_FOUND, "Can't find this user")
    return render_template(
        "user.j2",
        user=user,
        certification=get_certification_url(user),
        syllabus=get_syllabus(),
    )
