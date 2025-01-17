from app.database import engine
from app import models

def reset_db():
    print("Dropping all tables...")
    models.Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_db()
