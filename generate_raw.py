import random
import csv

random.seed(42)

# Real, well-known UEFA Champions League top scorers with realistic club/nationality mapping
players = [
    ("Cristiano Ronaldo", "Portugal", ["Manchester United", "Real Madrid", "Juventus"]),
    ("Lionel Messi", "Argentina", ["Barcelona", "Paris Saint-Germain"]),
    ("Robert Lewandowski", "Poland", ["Borussia Dortmund", "Bayern Munich", "Barcelona"]),
    ("Karim Benzema", "France", ["Real Madrid"]),
    ("Raul Gonzalez", "Spain", ["Real Madrid"]),
    ("Ruud van Nistelrooy", "Netherlands", ["Manchester United", "Real Madrid"]),
    ("Thomas Muller", "Germany", ["Bayern Munich"]),
    ("Kylian Mbappe", "France", ["Paris Saint-Germain", "Real Madrid"]),
    ("Alfredo Di Stefano", "Argentina", ["Real Madrid"]),
    ("Neymar Jr", "Brazil", ["Barcelona", "Paris Saint-Germain"]),
    ("Zlatan Ibrahimovic", "Sweden", ["Inter Milan", "Barcelona", "AC Milan", "Paris Saint-Germain"]),
    ("Andriy Shevchenko", "Ukraine", ["AC Milan", "Chelsea"]),
    ("Mohamed Salah", "Egypt", ["Liverpool"]),
    ("Erling Haaland", "Norway", ["Borussia Dortmund", "Manchester City"]),
    ("Sergio Aguero", "Argentina", ["Manchester City"]),
    ("Filippo Inzaghi", "Italy", ["AC Milan"]),
    ("Didier Drogba", "Ivory Coast", ["Chelsea"]),
    ("Wayne Rooney", "England", ["Manchester United"]),
    ("Alessandro Del Piero", "Italy", ["Juventus"]),
    ("Luis Suarez", "Uruguay", ["Barcelona", "Atletico Madrid"]),
    ("Fernando Torres", "Spain", ["Liverpool", "Chelsea"]),
    ("Antoine Griezmann", "France", ["Atletico Madrid"]),
    ("Harry Kane", "England", ["Tottenham Hotspur", "Bayern Munich"]),
    ("Kevin De Bruyne", "Belgium", ["Manchester City"]),
    ("Sadio Mane", "Senegal", ["Liverpool", "Bayern Munich"]),
    ("Gareth Bale", "Wales", ["Real Madrid"]),
    ("Toni Kroos", "Germany", ["Real Madrid"]),
    ("Luka Modric", "Croatia", ["Real Madrid"]),
    ("Vinicius Junior", "Brazil", ["Real Madrid"]),
    ("Julian Alvarez", "Argentina", ["Manchester City"]),
    ("Jude Bellingham", "England", ["Real Madrid"]),
    ("Bukayo Saka", "England", ["Arsenal"]),
    ("Victor Osimhen", "Nigeria", ["Napoli"]),
    ("Ousmane Dembele", "France", ["Barcelona", "Paris Saint-Germain"]),
    ("Joshua Kimmich", "Germany", ["Bayern Munich"]),
    ("Bernardo Silva", "Portugal", ["Manchester City"]),
    ("Riyad Mahrez", "Algeria", ["Manchester City"]),
    ("Paulo Dybala", "Argentina", ["Juventus"]),
    ("Edinson Cavani", "Uruguay", ["Paris Saint-Germain"]),
    ("Memphis Depay", "Netherlands", ["Barcelona"]),
]

seasons = [f"{y}-{str(y+1)[2:]}" for y in range(2010, 2024)]
rounds = ["Group Stage", "Round of 16", "Quarter-final", "Semi-final", "Final", "Group stage", "GROUP STAGE", "R16"]
goal_types = ["Right Foot", "Left Foot", "Header", "Penalty", "Free Kick", "right foot", "PENALTY", "header"]
venues = ["Home", "Away", "home", "AWAY", "Home ", " Away"]

opponents = ["Bayern Munich", "Real Madrid", "Barcelona", "Manchester United", "Manchester City",
             "Liverpool", "Chelsea", "Juventus", "AC Milan", "Inter Milan", "Paris Saint-Germain",
             "Borussia Dortmund", "Atletico Madrid", "Arsenal", "Tottenham Hotspur", "Porto",
             "Ajax", "Napoli", "Sevilla", "Benfica", None, ""]

rows = []
for i in range(2000):
    name, nat, clubs = random.choice(players)
    club = random.choice(clubs)
    season = random.choice(seasons)
    rnd = random.choice(rounds)
    minute = random.randint(1, 96)
    gtype = random.choice(goal_types)
    venue = random.choice(venues)
    opp = random.choice(opponents)
    goals_in_match = random.choice([1, 1, 1, 1, 2, 2, 3])

    # introduce messiness intentionally (to simulate raw scraped data)
    player_name = name
    if random.random() < 0.05:
        player_name = "  " + player_name.upper() + "  "   # extra spaces + wrong case
    if random.random() < 0.03:
        player_name = name.lower()

    minute_val = str(minute)
    if random.random() < 0.04:
        minute_val = f"{minute}'"       # scraped with apostrophe like "45'"
    if random.random() < 0.02:
        minute_val = ""                  # missing value

    club_val = club
    if random.random() < 0.03:
        club_val = club + "  "

    nat_val = nat
    if random.random() < 0.02:
        nat_val = None

    rows.append({
        "Player": player_name,
        "Nationality": nat_val,
        "Club": club_val,
        "Season": season,
        "Round": rnd,
        "Opponent": opp,
        "Minute": minute_val,
        "Goal_Type": gtype,
        "Venue": venue,
        "Goals_In_Match": goals_in_match,
    })

# inject duplicate rows (common scraping artifact)
dupes = random.sample(rows, 40)
rows.extend(dupes)

random.shuffle(rows)

with open("ucl_goal_scorers_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Total rows written: {len(rows)}")
