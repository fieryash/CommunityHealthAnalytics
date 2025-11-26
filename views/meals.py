import streamlit as st
from utils.scoring import calculate_personal_score
from utils.coach import Coach

def show():
    st.title("Order Meals 🛵")
    st.caption("Healthy meals from our premium partners.")
    
    coach = Coach(mode=st.session_state.get('coach_mode', 'Easy'))
    user_id = st.session_state['current_user_id']
    activity_df = st.session_state['activity_df']
    food_df = st.session_state['food_df']
    user_activity = activity_df[activity_df['user_id'] == user_id]
    
    # 1. Global Block: Missed Gym 3 days (Tough Love)
    is_globally_blocked = coach.check_cheat_meal_block(user_activity)
    
    # 2. Conditional Block: Low Health Score + Accountability Mode
    health_score = calculate_personal_score(activity_df, food_df, user_id)
    is_junk_blocked = False
    if st.session_state.get('coach_mode') == 'Accountability' and health_score < 70:
        is_junk_blocked = True
    
    if is_globally_blocked:
        st.error("🚫 ORDERING BLOCKED. Tough love <3 ! You missed the gym 3 days in a row.")
        st.info("Complete 10 consecutive valid gym sessions to unlock ordering.")
    elif is_junk_blocked:
        st.warning(f"⚠️ CHEAT MEALS BLOCKED. Your Health Score ({health_score}) is too low for cheat meals in Accountability Mode.")
    
    # Mock Partners Data
    partners = [
        {
            "name": "Cult.fit",
            "logo": "💪",
            "meals": [
                {"name": "High Protein Chicken Bowl", "cals": 450, "price": 250, "is_junk": False, "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"},
                {"name": "Quinoa & Veggie Salad", "cals": 320, "price": 200, "is_junk": False, "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"},
                {"name": "Cheat Burger (Weekend Special)", "cals": 850, "price": 300, "is_junk": True, "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd"},
            ]
        },
        {
            "name": "EatFit",
            "logo": "🥗",
            "meals": [
                {"name": "Dal Makhani & Roti", "cals": 600, "price": 180, "is_junk": False, "img": "https://images.unsplash.com/photo-1585937421612-70a008356f36"},
                {"name": "Chocolate Brownie", "cals": 400, "price": 120, "is_junk": True, "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d"},
                {"name": "Loaded Fries", "cals": 550, "price": 150, "is_junk": True, "img": "https://images.unsplash.com/photo-1573080496987-a199f8cd75ec"},
            ]
        },
        {
            "name": "HealthifyMe",
            "logo": "🥑",
            "meals": [
                {"name": "Keto Avocado Toast", "cals": 350, "price": 220, "is_junk": False, "img": "https://images.unsplash.com/photo-1588137372308-15f75323ca8d"},
                {"name": "Protein Pancakes", "cals": 400, "price": 240, "is_junk": False, "img": "https://images.unsplash.com/photo-1506084868230-bb9d95c24759"},
            ]
        }
    ]
    
    # Partner Tabs
    tabs = st.tabs([f"{p['logo']} {p['name']}" for p in partners])
    
    for i, tab in enumerate(tabs):
        with tab:
            partner = partners[i]
            st.subheader(f"Menu from {partner['name']}")
            
            cols = st.columns(len(partner['meals']))
            for j, meal in enumerate(partner['meals']):
                with cols[j]:
                    st.image(meal['img'], use_container_width=True)
                    st.write(f"**{meal['name']}**")
                    
                    # Metadata
                    meta = f"{meal['cals']} kcal | ₹{meal['price']}"
                    if meal.get('is_junk'):
                        st.markdown(f"{meta} <span style='color:red; font-weight:bold; border:1px solid red; padding:2px; border-radius:4px;'>CHEAT MEAL</span>", unsafe_allow_html=True)
                    else:
                        st.caption(meta)
                    
                    # Button Logic
                    btn_key = f"btn_{i}_{j}"
                    
                    if is_globally_blocked:
                        st.button(f"Order {meal['name']}", key=btn_key, disabled=True, help="Ordering blocked by Coach (Missed Gym)")
                    elif meal.get('is_junk') and is_junk_blocked:
                        st.button(f"Order {meal['name']}", key=btn_key, disabled=True, help=f"Blocked: Health Score {health_score} < 70")
                    else:
                        if st.button(f"Order {meal['name']}", key=btn_key):
                            if meal.get('is_junk'):
                                st.toast("Cheat meal ordered... Coach is watching 👀")
                            else:
                                st.balloons()
                                st.success(f"Order placed for {meal['name']}!")
