import streamlit as st
from utils.gamification import get_badges
from utils.scoring import calculate_personal_score

def show():
    st.title("Profile 👤")
    
    user = st.session_state['current_user']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=" + user['name'], width=200)
        
    with col2:
        st.header(user['name'])
        st.write(f"**Tower:** {user['tower_id']}")
        st.write(f"**Age:** {user['age']}")
        st.write(f"**Subscription:** {user['subscription_tier']}")
        
    st.divider()
    
    st.subheader("Badges & Achievements")
    
    # Calculate stats for badges
    user_id = st.session_state['current_user_id']
    activity_df = st.session_state['activity_df']
    food_df = st.session_state['food_df']
    
    score = calculate_personal_score(activity_df, food_df, user_id)
    
    # Mock streak
    streak = 12 
    
    badges = get_badges(score, streak)
    
    if badges:
        cols = st.columns(len(badges))
        for i, badge in enumerate(badges):
            cols[i].success(badge)
    else:
        st.info("Keep working out to earn badges!")
        
    st.divider()
    st.subheader("Settings")
    
    # Coach Mode (Global Setting)
    st.write("### 🤖 AI Coach Persona")
    current_mode = st.session_state.get('coach_mode', 'Easy')
    new_mode = st.radio(
        "Select your Coach's personality:",
        ["Easy", "Accountability"],
        index=0 if current_mode == "Easy" else 1,
        horizontal=True,
        help="Easy: Supportive and gentle. Accountability: Tough love and strict."
    )
    st.session_state['coach_mode'] = new_mode
    
    st.divider()
    st.toggle("Enable Notifications", value=True)
    st.toggle("Share Data with Tower", value=True)
