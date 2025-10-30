from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .Chat import Chat
from .ChatHistory import ChatHistory