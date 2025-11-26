import streamlit as st
import os
from utils.coach import Coach
from utils.scoring import calculate_personal_score

def show():
    st.title("AI Coach 🤖")
    
    # API Key Handling
    api_key = None
    
    # 1. Try Streamlit Secrets
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        
    # 2. Try Environment Variable
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    # 3. Try Sidebar Input
    if not api_key:
        api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
        if not api_key:
            st.warning("Please configure your API Key in .streamlit/secrets.toml or enter it in the sidebar.")
            return

    # Mode Selection (Now in Profile)
    mode = st.session_state.get('coach_mode', 'Easy')
    st.caption(f"Current Persona: **{mode}** (Change in Profile)")
    
    # Initialize Coach
    coach = Coach(mode=mode, api_key=api_key)
    
    # Prepare Context Stats
    user_id = st.session_state['current_user_id']
    activity_df = st.session_state['activity_df']
    food_df = st.session_state['food_df']
    user_activity = activity_df[activity_df['user_id'] == user_id]
    user_food = food_df[food_df['user_id'] == user_id]
    
    recent_activity = user_activity.sort_values('date', ascending=False).head(3)
    missed_gym = 3 - recent_activity[recent_activity['is_gym_valid']].shape[0]
    recent_cheats = user_food.sort_values('date', ascending=False).head(7)[user_food['is_cheat']].shape[0]
    health_score = calculate_personal_score(activity_df, food_df, user_id)
    
    stats = {
        "steps": user_activity['steps'].mean(),
        "missed_gym_days": missed_gym,
        "recent_cheats": recent_cheats,
        "health_score": health_score
    }
    
    # Chat Interface
    st.subheader(f"Chat with {mode} Coach")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me about your health..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Generate response
        with st.spinner("Coach is thinking..."):
            # Pass history excluding the current prompt which is handled by the method
            # Actually, my generate_response method takes user_input and history separately
            # So I should pass the history BEFORE this new message
            response = coach.generate_response(prompt, stats, st.session_state.messages)
        
        # Add user message to history NOW (after generation, or before? 
        # usually before, but my method takes history as 'past' context. 
        # Let's add user msg to state first, but pass 'messages[:-1]' to function? 
        # Or just pass messages and let function handle. 
        # The function `generate_response` takes `chat_history`. 
        # If I append user msg to session_state first, I should pass that.
        # But `chat.send_message(user_input)` appends the user input to history automatically in the backend object.
        # So I should pass the *previous* history to `chats.create`.
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
