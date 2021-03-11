import json

from certifications.config import SYLLABUS_PATH


def get_syllabus():
    return json.loads(SYLLABUS_PATH.read_text())
