from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product

fake = Faker()

def compute_information_score(category: str, description: str, attributes: dict) -> int:
    score = 0
    if description and len(description) >= 80:
        score += 1
    if category == "electronics" and attributes.get("battery_life_hours") is not None:
        score += 1
    if category == "grocery":
        if attributes.get("is_gluten_free") is not None: score += 1
        if attributes.get("is_high_fiber") is not None: score += 1
    return score

def main():
    db = SessionLocal()
    try:
        # Clear old data
        db.query(Product).delete()
        
        # Seed Electronics (10 items)
        for _ in range(10):
            attr = {"battery_life_hours": fake.random_int(min=12, max=72)}
            desc = fake.text(max_nb_chars=120)
            p = Product(name=f"{fake.word().title()} Smartwatch", category="electronics", description=desc)
            p.set_attributes(attr)
            p.information_score = compute_information_score("electronics", desc, attr)
            db.add(p)

        # Seed Grocery (15 items)
        for _ in range(15):
            desc = fake.sentence(nb_words=15)
            attr = {"is_gluten_free": fake.boolean(), "is_high_fiber": fake.boolean()}
            p = Product(name=fake.word().title(), category="grocery", description=desc)
            p.set_attributes(attr)
            p.information_score = compute_information_score("grocery", desc, attr)
            db.add(p)
            
        db.commit()
        print("Successfully seeded 25 products!")
    finally:
        db.close()

if __name__ == "__main__":
    main()