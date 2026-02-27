import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app import models
from app.auth.password_utils import hash_password
from datetime import datetime

def init_test_data():
    """Initialize database with test data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(models.User).filter(models.User.username == "testuser").first()
        if existing_user:
            print("Test user already exists.")
        else:
            # Create test user
            test_user = models.User(
                username="testuser",
                hashed_password=hash_password("password123")
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"Created test user: {test_user.username} (id={test_user.id})")
            
            # Create portfolio entry
            portfolio = models.Portfolio(
                user_id=test_user.id,
                symbol="AAPL",
                quantity=10,
                buy_price=150.0,
                buy_date=datetime.utcnow()
            )
            db.add(portfolio)
            
            # Create alert
            alert = models.Alert(
                user_id=test_user.id,
                symbol="AAPL",
                threshold=160.0,
                direction="above"
            )
            db.add(alert)
            
            db.commit()
            print("Created test portfolio: AAPL - 10 shares @ $150")
            print("Created test alert: AAPL - threshold $160 (above)")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Done.")

if __name__ == "__main__":
    init_test_data()
