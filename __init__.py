from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from blog import routes, models

@app.shell_context_processor
def make_shell_context():
  return {
    "db": db,
    "Entry": models.Entry
  }