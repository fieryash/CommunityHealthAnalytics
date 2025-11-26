import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
from .models import User, ActivityLog, FoodLog, Macro

fake = Faker()

TOWER_NAMES = [f"Tower {chr(65+i)}" for i in range(10)] # Tower A to J

def generate_users(n=100):
    users = []
    for _ in range(n):
        users.append({
            "id": fake.uuid4(),
            "name": fake.name(),
            "tower_id": random.choice(TOWER_NAMES),
            "age": random.randint(18, 80),
            "weight_kg": random.randint(50, 100),
            "height_cm": random.randint(150, 200),
            "subscription_tier": random.choice(['Basic', 'Premium', 'Pro'])
        })
    return pd.DataFrame(users)

def generate_activity_logs(user_ids, days=30):
    logs = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    for uid in user_ids:
        current_date = start_date
        while current_date <= end_date:
            steps = int(np.random.normal(6000, 2000))
            gym_mins = 0
            if random.random() > 0.6: # 40% chance of gym
                gym_mins = random.randint(5, 90)
            
            reading_mins = random.randint(0, 60)
            
            logs.append({
                "user_id": uid,
                "date": current_date.date(),
                "steps": max(0, steps),
                "gym_minutes": gym_mins,
                "is_gym_valid": gym_mins >= 10,
                "reading_minutes": reading_mins
            })
            current_date += timedelta(days=1)
            
    return pd.DataFrame(logs)

def generate_food_logs(user_ids, days=30):
    logs = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    sources = ['Zomato', 'Swiggy', 'MealPlan', 'Home']
    
    for uid in user_ids:
        current_date = start_date
        while current_date <= end_date:
            # Generate 3 meals per day
            for _ in range(3):
                source = random.choice(sources)
                is_cheat = False
                calories = int(np.random.normal(600, 100))
                
                if source in ['Zomato', 'Swiggy']:
                    if random.random() > 0.7: # 30% chance of junk from delivery
                        is_cheat = True
                        calories += 400
                
                logs.append({
                    "user_id": uid,
                    "date": current_date.date(),
                    "source": source,
                    "meal_name": f"Meal from {source}",
                    "calories": calories,
                    "protein": random.randint(10, 50),
                    "carbs": random.randint(30, 100),
                    "fat": random.randint(10, 40),
                    "is_cheat": is_cheat
                })
            current_date += timedelta(days=1)
            
    return pd.DataFrame(logs)

def get_tower_stats(users_df, activity_df, food_df):
    # Aggregate data by tower
    merged = users_df.merge(activity_df, left_on='id', right_on='user_id')
    
    tower_stats = []
    for tower in TOWER_NAMES:
        tower_users = users_df[users_df['tower_id'] == tower]
        tower_activity = merged[merged['tower_id'] == tower]
        
        # Calculate scores
        avg_steps = tower_activity['steps'].mean()
        gym_participation = tower_activity[tower_activity['gym_minutes'] > 0].shape[0] / len(tower_activity) if len(tower_activity) > 0 else 0
        
        tower_stats.append({
            "tower_id": tower,
            "population": len(tower_users),
            "avg_steps": int(avg_steps) if not np.isnan(avg_steps) else 0,
            "gym_participation_rate": round(gym_participation * 100, 1),
            "health_score": random.randint(60, 95) # Placeholder for complex scoring logic
        })
        
    return pd.DataFrame(tower_stats)
