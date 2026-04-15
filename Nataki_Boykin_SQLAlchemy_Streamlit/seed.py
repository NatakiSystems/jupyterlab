from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Post, Comment
import random

fake = Faker()

def seed_data():
    db = SessionLocal()
    
    # Create 10 Users
    users = []
    for i in range(10):
        user = User(
            email=fake.email(),
            name=fake.name(),
            role=random.choice(["admin", "editor", "user"])
        )
        db.add(user)
        users.append(user)
    
    db.commit()

    # Create 3 Posts for each user
    for user in users:
        for _ in range(3):
            post = Post(
                title=fake.sentence(),
                content=fake.paragraph(),
                author_id=user.id
            )
            db.add(post)
            db.flush() # Gets the post ID so we can add comments to it

            # Create 2 Comments for each post
            for _ in range(2):
                comment = Comment(
                    text=fake.sentence(),
                    author_id=random.choice(users).id,
                    post_id=post.id
                )
                db.add(comment)

    db.commit()
    db.close()
    print("Seeding complete! 10 users, 30 posts, and 60 comments created.")

if __name__ == "__main__":
    seed_data()