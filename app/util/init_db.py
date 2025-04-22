from app.core.database import Base, engine
from app.db.models import admin
from app.db.models import students

def create_tables():
    Base.metadata.create_all(bind=engine)