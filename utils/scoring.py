import pandas as pd
import numpy as np

def calculate_personal_score(activity_df, food_df, user_id):
    """
    Calculates a health score (0-100) for a specific user based on:
    - Steps (Target: 10k)
    - Gym Consistency (Target: 3x/week)
    - Nutrition (Cheat meal ratio)
    - Reading (Bonus)
    """
    user_activity = activity_df[activity_df['user_id'] == user_id]
    user_food = food_df[food_df['user_id'] == user_id]
    
    if user_activity.empty:
        return 50 # Default score
        
    # 1. Steps Score (30%)
    avg_steps = user_activity['steps'].mean()
    steps_score = min(100, (avg_steps / 10000) * 100)
    
    # 2. Gym Score (30%)
    # Count valid gym sessions in last 7 days
    recent_activity = user_activity.sort_values('date', ascending=False).head(7)
    valid_gym_days = recent_activity[recent_activity['is_gym_valid']].shape[0]
    gym_score = min(100, (valid_gym_days / 3) * 100) # Target 3 days a week
    
    # 3. Nutrition Score (30%)
    # Cheat meal ratio. Target < 20%
    total_meals = len(user_food)
    cheat_meals = user_food[user_food['is_cheat']].shape[0]
    if total_meals > 0:
        cheat_ratio = cheat_meals / total_meals
        nutrition_score = max(0, 100 - (cheat_ratio * 200)) # Penalize heavily
    else:
        nutrition_score = 50
        
    # 4. Wellbeing Score (10%)
    avg_reading = user_activity['reading_minutes'].mean()
    reading_score = min(100, (avg_reading / 30) * 100) # Target 30 mins
    
    final_score = (steps_score * 0.3) + (gym_score * 0.3) + (nutrition_score * 0.3) + (reading_score * 0.1)
    return int(final_score)

def calculate_tower_score(tower_users_df, activity_df, food_df):
    """
    Aggregates personal scores to get tower score.
    """
    scores = []
    for uid in tower_users_df['id'].unique():
        scores.append(calculate_personal_score(activity_df, food_df, uid))
        
    if not scores:
        return 0
        
    return int(np.mean(scores))
