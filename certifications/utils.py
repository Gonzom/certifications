import json
import secrets
import string
from typing import Dict, List, Union

from certifications.config import SYLLABUS_PATH


randomizer = secrets.SystemRandom()


def get_syllabus() -> List[Dict[str, Union[str, Dict[str, str]]]]:
    return json.loads(SYLLABUS_PATH.read_text(encoding='utf-8'))


def get_random_id(size: int = 8) -> str:
    chars = randomizer.choices(string.ascii_letters + string.digits, k=size)
    return ''.join(chars)
