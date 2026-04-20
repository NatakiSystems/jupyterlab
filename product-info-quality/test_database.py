import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase, Product

# This fixture connects to your real seeded database
@pytest.fixture(scope="module")
def seeded_session():
    engine = create_engine("sqlite:///test.db")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

# Test 1: Verify 25 products exist
def test_products_were_seeded(seeded_session):
    count = seeded_session.query(Product).count()
    assert count == 25, f"Expected 25 products, but found {count}"

# Test 2: Verify category breakdown (10 electronics, 15 grocery)
def test_both_categories_exist(seeded_session):
    electronics = seeded_session.query(Product).filter_by(category="electronics").count()
    grocery = seeded_session.query(Product).filter_by(category="grocery").count()
    assert electronics == 10, f"Expected 10 electronics, but found {electronics}"
    assert grocery == 15, f"Expected 15 grocery products, but found {grocery}"

# Test 3: Verify no products are missing barcode or price
def test_all_products_have_barcode_and_price(seeded_session):
    missing = seeded_session.query(Product).filter(
        (Product.barcode == None) | (Product.price == None)
    ).count()
    assert missing == 0, f"{missing} products are missing a barcode or price"