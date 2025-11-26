import streamlit as st
from components.charts import plot_tower_comparison

def show():
    st.title("Tower Analytics 🏢")
    st.caption("Aggregated public data for all 10 towers.")
    
    tower_stats = st.session_state['tower_stats_df']
    
    # Top Level Aggregates
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Population", f"{tower_stats['population'].sum():,}")
    with col2:
        st.metric("Avg Health Score", f"{int(tower_stats['health_score'].mean())}")
    with col3:
        st.metric("Active Gym Goers", f"{int(tower_stats['gym_participation_rate'].mean())}%")
        
    st.divider()
    
    # Charts
    st.subheader("Health Score Comparison")
    st.plotly_chart(plot_tower_comparison(tower_stats), use_container_width=True)
    
    # Detailed Data Table
    st.subheader("Tower Details")
    st.dataframe(
        tower_stats,
        column_config={
            "tower_id": "Tower",
            "population": "Residents",
            "avg_steps": "Avg Steps",
            "gym_participation_rate": st.column_config.ProgressColumn(
                "Gym Participation",
                format="%f%%",
                min_value=0,
                max_value=100,
            ),
            "health_score": "Health Score"
        },
        hide_index=True,
        use_container_width=True
    )
