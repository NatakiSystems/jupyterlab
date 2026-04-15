import streamlit as st
from sqlalchemy.orm import selectinload
from database import SessionLocal
from models import User, Post, Comment

def get_users():
    with SessionLocal() as db:
        return (
            db.query(User)
            .options(selectinload(User.posts).selectinload(Post.comments))
            .all()
        )

def main():
    st.set_page_config(page_title="Blog Explorer", layout="wide")
    st.title("🌐 Blog Explorer (SQLAlchemy + SQLite + Streamlit)")

    users = get_users()

    if not users:
        st.warning("No users found in the database. Run the seeder first.")
        st.stop()

    # Sidebar for navigation
    st.sidebar.header("Select a User")
    selected_user = st.sidebar.selectbox(
        "Users",
        users,
        format_func=lambda u: u.name
    )

    # Main Display
    st.subheader(f"Posts by {selected_user.name}")
    
    for post in selected_user.posts:
        with st.expander(post.title, expanded=False):
            st.write(post.content)
            
            st.markdown("**Comments:**")
            if post.comments:
                for comment in post.comments:
                    st.markdown(f"- {comment.text}")
            else:
                st.markdown("_No comments for this post._")

if __name__ == "__main__":
    main()