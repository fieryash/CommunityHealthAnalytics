import streamlit as st

def metric_card(label, value, delta=None, help_text=None):
    """
    Displays a metric card with optional delta and help text.
    """
    st.metric(label=label, value=value, delta=delta, help=help_text)

def custom_card(title, content, color="#FFFFFF"):
    """
    A custom card container with HTML/CSS styling.
    """
    st.markdown(
        f"""
        <div style="
            background-color: {color};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        ">
            <h3 style="margin-top: 0;">{title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
