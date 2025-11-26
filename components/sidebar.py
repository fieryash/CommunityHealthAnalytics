import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Township Health")
        
        page = st.radio(
            "Navigate",
            ["Dashboard", "Tower Analytics", "Leaderboard", "Meal Plans", "Coach", "Profile"]
        )
        
        st.divider()
        st.caption("v1.0.0 | Health Analytics")
        
        return page
