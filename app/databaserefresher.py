import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import db, create_app

app = create_app()

with app.app_context():
    db.drop_all()
    print("🗑 Все таблицы удалены.")
    db.create_all()
    print("✅ База данных пересоздана.")
    print("📋 Таблицы:", db.metadata.tables.keys())
