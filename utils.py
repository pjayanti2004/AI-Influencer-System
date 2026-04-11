
# Niche detection (rule-based AI)

def ai_detect_niche(bio):
    try:
        bio = str(bio).lower()

        if "tech" in bio or "gadget" in bio or "ai" in bio:
            return "Tech"
        elif "food" in bio or "chef" in bio:
            return "Food"
        elif "travel" in bio or "vlog" in bio:
            return "Travel"
        elif "fitness" in bio or "gym" in bio or "trainer" in bio:
            return "Fitness"
        else:
            return "Other"

    except:
        return "Other"


# Score calculation 

def calculate_score(followers, engagement, views, cost):
    try:
        # safe conversion
        followers = float(followers)
        engagement = float(engagement)
        views = float(views)
        cost = float(cost)

        # avoid divide by zero
        if cost == 0:
            return 0

        # SMART SCORE (performance per cost)
        score = (followers * engagement * views) / cost

        return round(score, 2)

    except:
        return 0