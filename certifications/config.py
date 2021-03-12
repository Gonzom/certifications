import pathlib


DOMAIN = 'certs.pythonic.guru'


CWD = pathlib.Path(__file__).parent
RESOURCES = CWD / 'resources'

DB_PATH = RESOURCES / 'students.db'
JSON_PATH = RESOURCES / 'students.json'
STATIC_PATH = CWD / 'static'
SYLLABUS_PATH = RESOURCES / 'syllabus.json'

CERT_PATH = RESOURCES / 'certificate'
CERT_FONT = CERT_PATH / 'OpenSansHebrew-regular.ttf'
CERT_IMAGE = CERT_PATH / 'certificate.png'
COURSE_AVATAR = CERT_PATH / 'avatar.png'
CERTS_FOLDER = STATIC_PATH / 'certifications'
