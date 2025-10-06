import app.services.user_service as user_service
import app.services.inventory_service as inventory_service
from app.db.session import SessionLocal, get_db


def seed_user_data(): 
    db = SessionLocal()

    # drop all existing users first 
    user_service.delete_all_users(db=db)

    user_service.create_user(db=db, name="Alan Zhu", email="alanzhukikak@gmail.com", hashed_password="hashed_password_123")
    user_service.create_user(db=db, name="John Doe", email="johndoe@example.com", hashed_password="hashed_password_456")

    db.close()


if __name__ == "__main__":
    seed_user_data()
