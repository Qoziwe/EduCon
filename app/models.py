from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import hashlib

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(255), default='default.png')
    bio = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.utcnow()  # Убедимся, что created_at установлен
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_avatar_url(self):
        return f'/static/usersdata/avatars/{self.avatar}'
    
    def save_avatar(self, file):
        # Удаляем старый аватар если он не дефолтный
        if self.avatar != 'default.png':
            old_path = os.path.join('app', 'static', 'usersdata', 'avatars', self.avatar)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # Генерируем хешированное имя файла
        filename = hashlib.md5((self.username + str(datetime.now())).encode()).hexdigest() + os.path.splitext(file.filename)[1]
        filepath = os.path.join('app', 'static', 'usersdata', 'avatars', filename)
        
        # Сохраняем файл
        file.save(filepath)
        self.avatar = filename
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'