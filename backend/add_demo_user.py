import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app import models
from app.auth.password_utils import hash_password

db = SessionLocal()
existing = db.query(models.User).filter(models.User.username == 'demo@demo.com').first()
print('demo user exists:', existing is not None)

if not existing:
    u = models.User(username='demo@demo.com', hashed_password=hash_password('demo123'))
    db.add(u)
    db.commit()
    print('Created demo user')
    
    # Add some portfolio items for demo user
    portfolio_items = [
        ('AAPL', 10, 150.0),
        ('GOOGL', 5, 2800.0),
        ('MSFT', 8, 300.0),
        ('TSLA', 3, 700.0),
        ('AMZN', 4, 3200.0),
        ('RELIANCE', 15, 2500.0),
    ]
    for symbol, qty, price in portfolio_items:
        p = models.Portfolio(user_id=u.id, symbol=symbol, quantity=qty, buy_price=price)
        db.add(p)
    db.commit()
    print('Added portfolio items for demo user')

db.close()
