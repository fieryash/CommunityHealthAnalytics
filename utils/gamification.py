def get_badges(user_score, gym_streak):
    badges = []
    if user_score > 80:
        badges.append("🌟 Health Nut")
    if user_score > 90:
        badges.append("🔥 Elite")
    if gym_streak > 5:
        badges.append("💪 Gym Rat")
    if gym_streak > 20:
        badges.append("🏋️ Iron Legend")
    return badges

def get_leaderboard_rewards(rank):
    if rank == 1:
        return "1 Month Maintenance FREE"
    elif rank == 2:
        return "15 Days Maintenance FREE"
    elif rank == 3:
        return "1 Week Maintenance FREE"
    return None
