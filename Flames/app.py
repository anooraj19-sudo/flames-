import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

VERDICTS = [
    {
        "title": "FRIEND ZONE",
        "emoji": "🤝",
        "message": "Some stories are better as friendships.\nAt least nobody has to argue over who replies first."
    },
    {
        "title": "LOVERS",
        "emoji": "❤️",
        "message": "The algorithm detected suspicious levels of chemistry.\nWhether reality agrees is a separate department."
    },
    {
        "title": "ATTRACTION",
        "emoji": "💘",
        "message": "There's definitely a spark.\nWhether someone sends the first message is beyond my processing power."
    },
    {
        "title": "MARRIAGE",
        "emoji": "💍",
        "message": "Congratulations!\nAccording to playground mathematics,\nyou may begin imaginary wedding preparations."
    },
    {
        "title": "ENEMIES",
        "emoji": "⚔️",
        "message": "Some people are soulmates.\nYou two are motivational villains."
    },
    {
        "title": "ONE NIGHT STAND",
        "emoji": "🌙",
        "message": "A brief chapter.\nLong-term planning apparently wasn't invited."
    },
    {
        "title": "STRANGERS",
        "emoji": "🚶",
        "message": "Two paths crossed for a moment,\nthen continued in different directions."
    },
    {
        "title": "SINGLE",
        "emoji": "😌",
        "message": "The algorithm recommends investing in yourself.\nNobody steals your fries."
    }
]


def remove_common(name1, name2):
    list1 = list(name1)
    list2 = list(name2)

    i = 0
    while i < len(list1):
        if list1[i] in list2:
            list2.remove(list1[i])
            list1.pop(i)
        else:
            i += 1

    return len(list1) + len(list2)


def flameoss_calc(count):
    options = VERDICTS.copy()
    index = 0

    while len(options) > 1:
        index = (index + count - 1) % len(options)
        options.pop(index)

    return options[0]


def generate_future(title, name1, name2):
    """Generates the future timeline payload based on the verdict title."""
    if title == "MARRIAGE":
        venues = ["Moonlight Garden", "A Beach Resort", "A Temple", "A Castle", "Under Water", "Las Vegas"]
        pets = ["Golden Retriever", "Orange Cat", "No Pets", "Three Cats", "A Dinosaur (probably)"]
        wealth = ["Rich", "Comfortable", "Middle Class", "Still paying EMIs"]
        return {
            "type": "MARRIAGE",
            "venue": random.choice(venues),
            "children": random.randint(0, 5),
            "pet": random.choice(pets),
            "wealth": random.choice(wealth),
            "divorce_chance": f"{random.randint(0, 30)}%",
            "years_together": random.randint(5, 80)
        }
    elif title == "LOVERS":
        dates = ["Pizza", "Coffee", "Movies", "A Walk", "Arcade"]
        return {
            "type": "LOVERS",
            "first_date": random.choice(dates),
            "texts_first": random.choice([name1, name2]),
            "shared_braincell": f"{random.randint(1, 100)}%",
            "first_kiss_days": random.randint(1, 365)
        }
    elif title == "FRIEND ZONE":
        return {
            "type": "FRIEND ZONE",
            "buys_food": random.choice([name1, name2]),
            "duration_years": random.randint(1, 80),
            "inside_jokes": random.randint(5, 500)
        }
    elif title == "ATTRACTION":
        return {
            "type": "ATTRACTION",
            "falls_first": random.choice([name1, name2]),
            "confession_success": f"{random.randint(40, 99)}%"
        }
    elif title == "ENEMIES":
        rival_types = ["Academic", "Gaming", "Workplace", "Childhood", "Unknown"]
        return {
            "type": "ENEMIES",
            "rival_type": random.choice(rival_types),
            "final_winner": random.choice([name1, name2, "Nobody"])
        }
    elif title == "ONE NIGHT STAND":
        calls = ["Never", "One", "Three", "Ghosted"]
        return {
            "type": "ONE NIGHT STAND",
            "calls_next_day": random.choice(calls),
            "awkwardness_level": f"{random.randint(1, 100)}%"
        }
    elif title == "STRANGERS":
        places = ["Airport", "Mall", "College", "Never"]
        return {
            "type": "STRANGERS",
            "remeet_chance": f"{random.randint(0, 40)}%",
            "likely_place": random.choice(places)
        }
    elif title == "SINGLE":
        friday_plans = ["Netflix", "Gaming", "Sleeping", "Coding", "Ordering Food"]
        relationship_status = ["Soon™", "Loading...", "Ask Again Later", "Unknown"]
        return {
            "type": "SINGLE",
            "friday_night": random.choice(friday_plans),
            "future_status": random.choice(relationship_status)
        }
    return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    raw1 = data.get('name1', '').strip()
    raw2 = data.get('name2', '').strip()

    if not raw1 or not raw2:
        return jsonify({'error': 'Both names are required'}), 400

    n1 = raw1.lower().replace(" ", "")
    n2 = raw2.lower().replace(" ", "")

    result = {}

    # Secret Self Love
    if n1 == n2:
        result = {
            "title": "SELF LOVE",
            "emoji": "💖",
            "message": "You entered the same name twice.\n\nBefore chasing someone else, remember that you're stuck with yourself forever.\nFortunately, that's not always a bad deal.",
            "allow_future": False
        }
    else:
        count = remove_common(n1, n2)

        # Cosmic Anomaly
        if count == 0:
            if random.choice([True, False]):
                result = {
                    "title": "PERFECT MATCH",
                    "emoji": "💖",
                    "message": "Every letter cancelled out.\n\nEven the algorithm stared into the void.\nApparently destiny approves.",
                    "allow_future": False
                }
            else:
                verdict = VERDICTS[7]
                result = {
                    "title": verdict["title"],
                    "emoji": verdict["emoji"],
                    "message": verdict["message"],
                    "allow_future": True
                }
        else:
            verdict = flameoss_calc(count)
            result = {
                "title": verdict["title"],
                "emoji": verdict["emoji"],
                "message": verdict["message"],
                "allow_future": True
            }

    # Generate future scan if applicable
    future_data = None
    if result.get("allow_future"):
        future_data = generate_future(result["title"], raw1, raw2)

    return jsonify({
        "result": result,
        "future": future_data,
        "name1": raw1,
        "name2": raw2
    })


if __name__ == '__main__':
    app.run(debug=True)