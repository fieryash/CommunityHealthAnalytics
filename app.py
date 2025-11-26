import streamlit as st
import pandas as pd
from components.sidebar import sidebar
from data.generator import generate_users, generate_activity_logs, generate_food_logs, get_tower_stats
from views import dashboard, tower, leaderboard, meals, coach, profile

# Page Config
st.set_page_config(
    page_title="Township Health Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'data_initialized' not in st.session_state:
    with st.spinner("Initializing Township Data..."):
        # Generate Mock Data
        users_df = generate_users(200)
        activity_df = generate_activity_logs(users_df['id'].tolist())
        food_df = generate_food_logs(users_df['id'].tolist())
        tower_stats_df = get_tower_stats(users_df, activity_df, food_df)
        
        st.session_state['users_df'] = users_df
        st.session_state['activity_df'] = activity_df
        st.session_state['food_df'] = food_df
        st.session_state['tower_stats_df'] = tower_stats_df
        
        # Set current user (for demo purposes, pick the first one)
        st.session_state['current_user_id'] = users_df.iloc[0]['id']
        st.session_state['current_user'] = users_df.iloc[0].to_dict()
        
        # Coach settings
        st.session_state['coach_mode'] = "Easy"
        
        st.session_state['data_initialized'] = True

# Navigation
page = sidebar()

# Routing
if page == "Dashboard":
    dashboard.show()
elif page == "Tower Analytics":
    tower.show()
elif page == "Leaderboard":
    leaderboard.show()
elif page == "Meal Plans":
    meals.show()
elif page == "Coach":
    coach.show()
elif page == "Profile":
    profile.show()
