import streamlit as st
import pandas as pd
from components.cards import metric_card
from components.charts import plot_steps_timeline, plot_gym_timeline, plot_macro_breakdown
from utils.scoring import calculate_personal_score

def show():
    st.title(f"Welcome back, {st.session_state['current_user']['name']}! 👋")
    
    user_id = st.session_state['current_user_id']
    activity_df = st.session_state['activity_df']
    food_df = st.session_state['food_df']
    
    user_activity = activity_df[activity_df['user_id'] == user_id]
    user_food = food_df[food_df['user_id'] == user_id]
    
    # Calculate Score
    score = calculate_personal_score(activity_df, food_df, user_id)
    
    # Top Row: Score & Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Health Score", f"{score}/100", delta=2)
    with col2:
        avg_steps = int(user_activity['steps'].mean())
        st.metric("Avg Steps", f"{avg_steps}", delta=500)
    with col3:
        valid_gym = user_activity[user_activity['is_gym_valid']].shape[0]
        st.metric("Gym Sessions", f"{valid_gym}", help="Valid sessions > 10 mins")
    with col4:
        avg_cal = int(user_food['calories'].mean())
        st.metric("Avg Calories", f"{avg_cal} kcal")
        
    st.divider()
    
    # Activity Graphs
    st.subheader("Activity Timeline")
    col_graph1, col_graph2 = st.columns(2)
    with col_graph1:
        st.plotly_chart(plot_steps_timeline(user_activity), use_container_width=True)
    with col_graph2:
        st.plotly_chart(plot_gym_timeline(user_activity), use_container_width=True)
    
    # Macros & Details
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Nutrition Breakdown (Avg)")
        avg_macros = {
            "Protein": user_food['protein'].mean(),
            "Carbs": user_food['carbs'].mean(),
            "Fat": user_food['fat'].mean()
        }
        st.plotly_chart(plot_macro_breakdown(avg_macros), use_container_width=True)
        
    with col_right:
        st.subheader("Recent Alerts")
        # Check for cheat meals
        recent_cheats = user_food[user_food['is_cheat']].tail(5)
        if not recent_cheats.empty:
            st.warning(f"Detected {len(recent_cheats)} cheat meals recently.")
            st.dataframe(recent_cheats[['date', 'meal_name', 'calories']], hide_index=True)
        else:
            st.success("Clean eating streak! Keep it up.")
            
        st.info(f"Reading Time: {int(user_activity['reading_minutes'].sum() / 60)} hours total")
