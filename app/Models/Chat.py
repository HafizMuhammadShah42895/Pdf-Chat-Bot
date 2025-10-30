from app.Models import db 
from datetime import datetime

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_name = db.Column(db.String(100))
    pdf_path = db.Column(db.String(255))
    custom_prompt = db.Column(db.Text)
    chromadb_collection = db.Column(db.String(100))
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
