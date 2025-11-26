from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Macro:
    protein: int
    carbs: int
    fat: int

@dataclass
class Meal:
    name: str
    calories: int
    macros: Macro
    is_cheat: bool
    image_url: str = "https://via.placeholder.com/150"

@dataclass
class User:
    id: str
    name: str
    tower_id: str
    age: int
    weight_kg: float
    height_cm: float
    subscription_tier: str # 'Basic', 'Premium', 'Pro'

@dataclass
class ActivityLog:
    date: datetime
    steps: int
    gym_minutes: int
    reading_minutes: int
    is_gym_valid: bool

@dataclass
class FoodLog:
    date: datetime
    meal_name: str
    calories: int
    macros: Macro
    source: str # 'Zomato', 'Swiggy', 'MealPlan', 'Home'
    is_cheat: bool
