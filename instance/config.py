import os

SECRET_KEY = 'p9Bv<3Eid9%$i01'
if os.getenv('FLASK_CONFIG') == "testing":
    SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_test'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'
