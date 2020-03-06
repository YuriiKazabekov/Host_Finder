from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap

######################
#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView


#######################################
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models
from app.models import db, User#, Post




# set optional bootswatch theme
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#admin = Admin(app, name='TSNetApp Admin', template_mode='bootstrap3')

#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Post, db.session))
#admin.add_view(ModelView(Role,  db.session, category="model"))






