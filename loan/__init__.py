from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app=Flask(__name__)

app.config['SECRET_KEY']='8c568937f79e5cc394a108a28ae6093d'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'



db=SQLAlchemy(app)
app.app_context().push()
bcrypt=Bcrypt(app)


from loan import routes