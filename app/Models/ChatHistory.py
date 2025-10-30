from datetime import datetime
from app.Models import db

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('chat_histories', cascade='all, delete-orphan'))
    chat = db.relationship('Chat', backref=db.backref('chat_histories', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<ChatHistory Q: {self.question[:20]} | A: {self.answer[:20]}>"



