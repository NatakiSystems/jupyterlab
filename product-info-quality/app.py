import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Product

# Helper to connect to the database
def get_session():
    return SessionLocal()

# Function to turn database objects into something Streamlit can read
def product_to_dict(p):
    return {
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "description": p.description,
        "information_score": p.information_score,
        "created_at": p.created_at
    }

def main():
    st.set_page_config(page_title="Product Quality Dashboard", layout="wide")
    st.title("Product Information Quality Dashboard")
    st.write("Analyze completeness and identify items that need better descriptions.")

    # SIDEBAR: Add a new product
    st.sidebar.header("Add New Product")
    with st.sidebar.form("add_form"):
        name = st.text_input("Product Name")
        cat = st.selectbox("Category", ["electronics", "grocery"])
        desc = st.text_area("Description")
        submitted = st.form_submit_button("Add Product")
        
        if submitted:
            session = get_session()
            new_p = Product(name=name, category=cat, description=desc)
            # We skip scoring logic here for simplicity to ensure the app runs
            session.add(new_p)
            session.commit()
            st.sidebar.success("Added!")
            st.rerun()

    # FILTERS
    st.sidebar.markdown("---")
    cat_filter = st.sidebar.selectbox("Filter by Category", ["all", "electronics", "grocery"])

    # DATABASE QUERY
    session = get_session()
    query = session.query(Product)
    if cat_filter != "all":
        query = query.filter(Product.category == cat_filter)
    products = query.all()
    session.close()

    # DATA TABLES
    rows = [product_to_dict(p) for p in products]
    
    st.subheader("All Products")
    st.dataframe(rows, use_container_width=True)

    # FLAG SYSTEM (Score < 2)
    st.subheader("Flagged Products (Inadequate Information)")
    flagged = [r for r in rows if r["information_score"] < 2]
    if flagged:
        st.warning(f"Found {len(flagged)} items with low information scores.")
        st.table(flagged)
    else:
        st.success("No products currently flagged!")

if __name__ == "__main__":
    main()