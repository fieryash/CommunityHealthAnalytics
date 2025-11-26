import streamlit as st
from utils.gamification import get_leaderboard_rewards

def show():
    st.title("Leaderboard 🏆")
    
    tower_stats = st.session_state['tower_stats_df'].sort_values('health_score', ascending=False).reset_index(drop=True)
    
    # Podium
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>🥇 {tower_stats.iloc[0]['tower_id']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Score: {tower_stats.iloc[0]['health_score']}</p>", unsafe_allow_html=True)
        st.success(f"Reward: {get_leaderboard_rewards(1)}")
        
    with col1:
        st.markdown(f"<h3 style='text-align: center;'>🥈 {tower_stats.iloc[1]['tower_id']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Score: {tower_stats.iloc[1]['health_score']}</p>", unsafe_allow_html=True)
        st.info(f"Reward: {get_leaderboard_rewards(2)}")
        
    with col3:
        st.markdown(f"<h3 style='text-align: center;'>🥉 {tower_stats.iloc[2]['tower_id']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Score: {tower_stats.iloc[2]['health_score']}</p>", unsafe_allow_html=True)
        st.warning(f"Reward: {get_leaderboard_rewards(3)}")
        
    st.divider()
    
    st.subheader("Full Rankings")
    for index, row in tower_stats.iterrows():
        rank = index + 1
        st.markdown(f"**{rank}. {row['tower_id']}** - Score: {row['health_score']}")
        st.progress(row['health_score'] / 100)
