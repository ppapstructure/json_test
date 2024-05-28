import os

BASE_DIR = os.path.dirname(__file__)

# mysql
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0000@db/mydatabase'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20180503@localhost/test'


SQLALCHEMY_TRACK_MODIFICATIONS = False
# POSTMAN에서 사용하기 위해서 임시 설정
WTF_CSRF_ENABLED = False
# 아래 설정으로 나중에 토큰 받아서 다시 실행
# secret key
SECRET_KEY = 'dev'

# 이메일 설정 
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587 # GOOGLE은 주로 587 사용
MAIL_USE_TLS = True
MAIL_USERNAME = 'skskfl5786@gmail.com'
# google 계정의 2단계 인증으로 인하여 앱비밀번호를 설정하여 임의의 비밀번호을 발급 받아 사용함.
MAIL_PASSWORD = 'cgzb ttij xpsm iljk'






# 내 로컬환경에선 root:20180503 localhost/test
# 내 도커환경에선 root:0000 db/mydatabase