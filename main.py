from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
import hashlib

app = FastAPI(
    title="Peregrine Run Club API",
    description="Synthetic Strava-like API for Run Club demo",
    version="1.0.0"
)

# Enable CORS for Peregrine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== ATHLETES ==============
ATHLETES = [
    {"athlete_id": "athlete_001", "name": "Aakash Pattabi", "office": "San Francisco"},
    {"athlete_id": "athlete_002", "name": "Aaron Nichol", "office": "San Francisco"},
    {"athlete_id": "athlete_003", "name": "Abigail Meisel", "office": "Washington DC"},
    {"athlete_id": "athlete_004", "name": "Aneesh Deshpande", "office": "San Francisco"},
    {"athlete_id": "athlete_005", "name": "Angela Lee", "office": "San Francisco"},
    {"athlete_id": "athlete_006", "name": "Arjun Patel", "office": "New York City"},
    {"athlete_id": "athlete_007", "name": "Ayush Kalani", "office": "San Francisco"},
    {"athlete_id": "athlete_008", "name": "Betty Hu", "office": "San Francisco"},
    {"athlete_id": "athlete_009", "name": "Brian Wong", "office": "San Francisco"},
    {"athlete_id": "athlete_010", "name": "Dave Ellery", "office": "San Francisco"},
    {"athlete_id": "athlete_011", "name": "Emily Dworkin", "office": "San Francisco"},
    {"athlete_id": "athlete_012", "name": "Ethan Taotafa", "office": "San Francisco"},
    {"athlete_id": "athlete_013", "name": "Hadley Irwin", "office": "San Francisco"},
    {"athlete_id": "athlete_014", "name": "Hersh Patel", "office": "New York City"},
    {"athlete_id": "athlete_015", "name": "Jim Krider", "office": "Washington DC"},
    {"athlete_id": "athlete_016", "name": "John Quinlan", "office": "San Francisco"},
    {"athlete_id": "athlete_017", "name": "Josh Pearson", "office": "Washington DC"},
    {"athlete_id": "athlete_018", "name": "James Pascoe-Price", "office": "Remote"},
    {"athlete_id": "athlete_019", "name": "Kat Summers", "office": "San Francisco"},
    {"athlete_id": "athlete_020", "name": "Laura Henn", "office": "San Francisco"},
    {"athlete_id": "athlete_021", "name": "Marc Palmieri", "office": "New York City"},
    {"athlete_id": "athlete_022", "name": "Martin Koppel", "office": "San Francisco"},
    {"athlete_id": "athlete_023", "name": "Meg Suave", "office": "Washington DC"},
    {"athlete_id": "athlete_024", "name": "Michael Gates", "office": "New York City"},
    {"athlete_id": "athlete_025", "name": "Natalie Blundell", "office": "San Francisco"},
    {"athlete_id": "athlete_026", "name": "Nick Alessi", "office": "San Francisco"},
    {"athlete_id": "athlete_027", "name": "Noa Mondeja", "office": "San Francisco"},
    {"athlete_id": "athlete_028", "name": "Ruby Cheng", "office": "San Francisco"},
    {"athlete_id": "athlete_029", "name": "Sagar Vemuri", "office": "New York City"},
    {"athlete_id": "athlete_030", "name": "Sarah Wiessler", "office": "New York City"},
    {"athlete_id": "athlete_031", "name": "Seth Jaffe", "office": "Washington DC"},
    {"athlete_id": "athlete_032", "name": "Shawn Blas", "office": "Remote"},
    {"athlete_id": "athlete_033", "name": "Simon Miera", "office": "Remote"},
    {"athlete_id": "athlete_034", "name": "Stacey Baradit", "office": "Remote"},
    {"athlete_id": "athlete_035", "name": "Viet Huynh", "office": "San Francisco"},
    {"athlete_id": "athlete_036", "name": "Will Tholke", "office": "San Francisco"},
    {"athlete_id": "athlete_037", "name": "Zach Bys", "office": "San Francisco"},
    {"athlete_id": "athlete_038", "name": "Zheng Mi", "office": "San Francisco"},
]

# Activity types and their typical characteristics
ACTIVITY_PROFILES = {
    "Run": {"min_dist": 2, "max_dist": 15, "min_speed": 5, "max_speed": 10},
    "Ride": {"min_dist": 5, "max_dist": 50, "min_speed": 10, "max_speed": 25},
    "Walk": {"min_dist": 1, "max_dist": 6, "min_speed": 2, "max_speed": 4},
    "Hike": {"min_dist": 3, "max_dist": 12, "min_speed": 2, "max_speed": 4},
    "Swim": {"min_dist": 0.25, "max_dist": 2, "min_speed": 1, "max_speed": 3},
}

# Athlete activity preferences (which sports they do)
def get_athlete_sports(athlete_id: str) -> List[str]:
    """Deterministically assign sports to each athlete"""
    seed = int(hashlib.md5(athlete_id.encode()).hexdigest(), 16)
    random.seed(seed)
    all_sports = list(ACTIVITY_PROFILES.keys())
    num_sports = random.randint(1, 4)
    # Everyone does at least Run
    sports = ["Run"] + random.sample([s for s in all_sports if s != "Run"], min(num_sports - 1, len(all_sports) - 1))
    return sports

# Logo Challenge polylines (simplified encoded polylines for demo)
LOGO_CHALLENGE = {
    "Will Tholke": {
        "park": "Golden Gate Park",
        "city": "San Francisco",
        "polyline": "ohreFfndjVmBcDgCeE_BgC}AgCwAcCqAcCiAcCoA_DsAcEuAaFqAaFoAcFiAaFcA}E}@yEs@wEk@uEc@sE_@qEYoEUmESiESgESmESiEWmE[oEc@sEg@wEq@yE}@cF",
        "distance_miles": 3.2,
        "activity_id": "logo_sf_001"
    },
    "Seth Jaffe": {
        "park": "National Mall / Memorial Park",
        "city": "Washington DC",
        "polyline": "w~llFtieuMcBaDoBcDcCcDgCaDkCaDmC_DoCyCoC{CqCyCsCyCuCwCwCuCsCqCoCmCkCiCgCeCaC_C{ByBwBsBoBkBgBcB}AyAuAqAmAiAeA",
        "distance_miles": 2.8,
        "activity_id": "logo_dc_001"
    },
    "Arjun Patel": {
        "park": "Central Park",
        "city": "New York City",
        "polyline": "cr_wFtdqbMkBqCoBwCmByCkB}CiBaDeB_DeByC_BuCyAqCsAmCoAgCkAaCeA}B_AyBw@uBq@qBm@mBg@iB",
        "distance_miles": 3.5,
        "activity_id": "logo_nyc_001"
    }
}

def generate_activity(athlete_id: str, athlete_name: str, date: datetime, activity_type: str, idx: int) -> dict:
    """Generate a synthetic activity"""
    profile = ACTIVITY_PROFILES[activity_type]
    athlete = next((a for a in ATHLETES if a["athlete_id"] == athlete_id), {})
    # Seed for reproducibility
    seed_str = f"{athlete_id}_{date.isoformat()}_{activity_type}_{idx}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)
    
    distance_miles = round(random.uniform(profile["min_dist"], profile["max_dist"]), 2)
    avg_speed = round(random.uniform(profile["min_speed"], profile["max_speed"]), 1)
    moving_time_min = round((distance_miles / avg_speed) * 60)
    elapsed_time_min = moving_time_min + random.randint(0, 15)
    elevation_gain = round(random.uniform(50, 500)) if activity_type in ["Run", "Ride", "Hike"] else 0
    
    # Activity names
    time_of_day = ["Morning", "Lunch", "Afternoon", "Evening"][random.randint(0, 3)]
    activity_names = {
        "Run": [f"{time_of_day} Run", "Easy Run", "Tempo Run", "Long Run", "Recovery Run"],
        "Ride": [f"{time_of_day} Ride", "Commute", "Weekend Ride", "Hill Climb", "Easy Spin"],
        "Walk": [f"{time_of_day} Walk", "Lunch Walk", "Dog Walk", "Evening Stroll"],
        "Hike": ["Trail Hike", "Weekend Hike", "Mountain Trek", "Nature Walk"],
        "Swim": ["Pool Swim", "Open Water", "Laps", "Recovery Swim"],
    }
    
    return {
        "activity_id": f"act_{athlete_id}_{date.strftime('%Y%m%d')}_{idx}",
        "athlete_id": athlete_id,
        "athlete_name": athlete_name,
        "name": random.choice(activity_names[activity_type]),
        "type": activity_type,
        "start_date": date.isoformat() + "Z",
        "start_date_local": date.isoformat(),
        "distance_miles": distance_miles,
        "moving_time_min": moving_time_min,
        "elapsed_time_min": elapsed_time_min,
        "average_speed_mph": avg_speed,
        "max_speed_mph": round(avg_speed * random.uniform(1.1, 1.4), 1),
        "total_elevation_gain_ft": elevation_gain,
        "calories": round(distance_miles * random.uniform(80, 120)),
        "is_logo_challenge": False,
        "summary_polyline": None,
        "office": athlete.get("office", "Unknown")
    }

def generate_activities_for_athlete(athlete: dict, start_date: datetime, end_date: datetime) -> List[dict]:
    """Generate 2 years of activities for an athlete"""
    activities = []
    sports = get_athlete_sports(athlete["athlete_id"])
    
    current = start_date
    while current <= end_date:
        # Seed for this day
        day_seed = int(hashlib.md5(f"{athlete['athlete_id']}_{current.isoformat()}".encode()).hexdigest(), 16)
        random.seed(day_seed)
        
        # 60% chance of activity on any given day
        if random.random() < 0.6:
            activity_type = random.choice(sports)
            hour = random.randint(5, 20)
            activity_time = current.replace(hour=hour, minute=random.randint(0, 59))
            activities.append(generate_activity(
                athlete["athlete_id"],
                athlete["name"],
                activity_time,
                activity_type,
                len(activities)
            ))
            
            # 20% chance of second activity
            if random.random() < 0.2:
                second_type = random.choice([s for s in sports if s != activity_type] or sports)
                second_time = current.replace(hour=min(hour + random.randint(4, 8), 22))
                activities.append(generate_activity(
                    athlete["athlete_id"],
                    athlete["name"],
                    second_time,
                    second_type,
                    len(activities)
                ))
        
        current += timedelta(days=1)
    
    return activities

# ============== API ENDPOINTS ==============

@app.get("/")
def root():
    return {
        "name": "Peregrine Run Club API",
        "version": "1.0.0",
        "athletes": len(ATHLETES),
        "date_range": "2024-01-01 to 2026-01-01"
    }

@app.get("/athletes")
def get_athletes(office: Optional[str] = Query(None, description="Filter by office")):
    """Get all athletes, optionally filtered by office"""
    if office:
        return [a for a in ATHLETES if a["office"].lower() == office.lower()]
    return ATHLETES

@app.get("/athletes/{athlete_id}")
def get_athlete(athlete_id: str):
    """Get a single athlete by ID"""
    athlete = next((a for a in ATHLETES if a["athlete_id"] == athlete_id), None)
    if athlete:
        athlete["sports"] = get_athlete_sports(athlete_id)
    return athlete

@app.get("/athletes/{athlete_id}/activities")
def get_athlete_activities(
    athlete_id: str,
    start_date: Optional[str] = Query("2024-01-01", description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query("2026-01-01", description="End date YYYY-MM-DD"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type")
):
    """Get activities for a specific athlete"""
    athlete = next((a for a in ATHLETES if a["athlete_id"] == athlete_id), None)
    if not athlete:
        return []
    
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    activities = generate_activities_for_athlete(athlete, start, end)
    
    if activity_type:
        activities = [a for a in activities if a["type"].lower() == activity_type.lower()]
    
    return activities

@app.get("/activities")
def get_all_activities(
    office: Optional[str] = Query(None),
    activity_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query("2024-01-01"),
    end_date: Optional[str] = Query("2026-01-01"),
    limit: int = Query(100, le=1000)
):
    """Get all activities across all athletes"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    athletes = ATHLETES
    if office:
        athletes = [a for a in athletes if a["office"].lower() == office.lower()]
    
    all_activities = []
    for athlete in athletes:
        activities = generate_activities_for_athlete(athlete, start, end)
        all_activities.extend(activities)
    
    if activity_type:
        all_activities = [a for a in all_activities if a["type"].lower() == activity_type.lower()]
    
    # Sort by date descending
    all_activities.sort(key=lambda x: x["start_date"], reverse=True)
    
    return all_activities[:limit]

@app.get("/stats")
def get_stats(
    office: Optional[str] = Query(None),
    start_date: Optional[str] = Query("2024-01-01"),
    end_date: Optional[str] = Query("2026-01-01")
):
    """Get aggregate stats"""
    activities = get_all_activities(office=office, start_date=start_date, end_date=end_date, limit=10000)
    
    total_distance = sum(a["distance_miles"] for a in activities)
    total_time = sum(a["moving_time_min"] for a in activities)
    
    by_type = {}
    for a in activities:
        t = a["type"]
        if t not in by_type:
            by_type[t] = {"count": 0, "distance_miles": 0}
        by_type[t]["count"] += 1
        by_type[t]["distance_miles"] += a["distance_miles"]
    
    by_office = {}
    for a in activities:
        athlete = next((at for at in ATHLETES if at["athlete_id"] == a["athlete_id"]), None)
        if athlete:
            o = athlete["office"]
            if o not in by_office:
                by_office[o] = {"count": 0, "distance_miles": 0}
            by_office[o]["count"] += 1
            by_office[o]["distance_miles"] += a["distance_miles"]
    
    return {
        "total_activities": len(activities),
        "total_distance_miles": round(total_distance, 1),
        "total_time_hours": round(total_time / 60, 1),
        "by_activity_type": by_type,
        "by_office": by_office
    }

@app.get("/logo-challenge")
def get_logo_challenge():
    """Get the Peregrine logo challenge activities"""
    challenges = []
    for name, data in LOGO_CHALLENGE.items():
        athlete = next((a for a in ATHLETES if a["name"] == name), None)
        if athlete:
            challenges.append({
                "activity_id": data["activity_id"],
                "athlete_id": athlete["athlete_id"],
                "athlete_name": name,
                "name": f"Peregrine Logo Challenge - {data['park']}",
                "type": "Run",
                "start_date": "2025-12-15T09:00:00Z",
                "distance_miles": data["distance_miles"],
                "park": data["park"],
                "city": data["city"],
                "is_logo_challenge": True,
                "summary_polyline": data["polyline"]
            })
    return challenges

@app.get("/offices")
def get_offices():
    """Get list of offices with athlete counts"""
    offices = {}
    for a in ATHLETES:
        o = a["office"]
        offices[o] = offices.get(o, 0) + 1
    return [{"office": k, "athlete_count": v} for k, v in offices.items()]
