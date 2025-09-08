from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config
from sqlalchemy import inspect

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Импорт моделей после инициализации db
    from app import models
    
    # Настройка login_manager
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'
    
    # Регистрация blueprint'ов
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Автоматическое создание таблиц при запуске приложения
    with app.app_context():
        # Проверяем, существует ли уже база данных
        inspector = inspect(db.engine)
        
        # Проверяем существование таблиц
        tables_exist = inspector.has_table('user')
        
        if not tables_exist:
            db.create_all()
            print("✅ База данных создана!")
        else:
            print("✅ База данных уже существует")
    
    return app