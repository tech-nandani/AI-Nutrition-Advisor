from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_diet_plan(food_preference):
    if food_preference == "Vegetarian":
        return {
            "breakfast": [
                "🥣 Oatmeal with Fruits",
                "🍌 Fresh Banana"
            ],
            "lunch": [
                "🍛 Dal & Roti",
                "🥗 Fresh Green Salad"
            ],
            "snack": [
                "🥜 Mixed Nuts",
                "🍎 Fresh Apple"
            ],
            "dinner": [
                "🥘 Paneer & Vegetables",
                "🍚 Brown Rice"
            ]
        }

    elif food_preference == "Non-Vegetarian":
        return {
            "breakfast": [
                "🥚 Boiled Eggs",
                "🍞 Whole Wheat Toast"
            ],
            "lunch": [
                "🍗 Grilled Chicken",
                "🍚 Brown Rice"
            ],
            "snack": [
                "🥜 Mixed Nuts",
                "🍎 Fresh Apple"
            ],
            "dinner": [
                "🐟 Grilled Fish",
                "🥗 Fresh Green Salad"
            ]
        }

    elif food_preference == "Vegan":
        return {
            "breakfast": [
                "🥣 Oatmeal with Soy Milk",
                "🍌 Fresh Banana"
            ],
            "lunch": [
                "🥗 Chickpea Salad",
                "🥬 Mixed Vegetables"
            ],
            "snack": [
                "🥜 Almonds & Walnuts",
                "🍎 Fresh Apple"
            ],
            "dinner": [
                "🍲 Tofu & Vegetables",
                "🍚 Brown Rice"
            ]
        }

    else:
        return {
            "breakfast": ["🥣 Healthy Oatmeal", "🍌 Fresh Banana"],
            "lunch": ["🍛 Balanced Meal", "🥗 Green Salad"],
            "snack": ["🥜 Mixed Nuts", "🍎 Fresh Apple"],
            "dinner": ["🥘 Healthy Dinner", "🍚 Brown Rice"]
        }
app.secret_key = "ai_nutrition_advisor_secret_key"
# ---------------- DATABASE ----------------

DATABASE = "nutrition.db"


def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_db_connection()

    connection.execute("""

        CREATE TABLE IF NOT EXISTS weight_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_name TEXT,

            weight REAL,

            date TEXT

        )

    """)

    connection.commit()

    connection.close()


initialize_database()

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- PROFILE ----------------

# ---------------- PROFILE ----------------

# ---------------- PROFILE ----------------

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":

        session["name"] = request.form.get("name")
        session["age"] = request.form.get("age")
        session["gender"] = request.form.get("gender")
        session["height"] = request.form.get("height")
        session["weight"] = request.form.get("weight")
        session["activity"] = request.form.get("activity")
        session["food_preference"] = request.form.get("food_preference")
        session["goal"] = request.form.get("goal")


        # ---------------- SAVE WEIGHT HISTORY ----------------

        connection = get_db_connection()

        today = datetime.now().strftime("%Y-%m-%d")


        # Check if today's weight already exists
        existing_weight = connection.execute(
            """
            SELECT id
            FROM weight_history
            WHERE user_name = ? AND date = ?
            """,
            (
                session.get("name"),
                today
            )
        ).fetchone()


        # Update existing weight
        if existing_weight:

            connection.execute(
                """
                UPDATE weight_history
                SET weight = ?
                WHERE user_name = ? AND date = ?
                """,
                (
                    float(session.get("weight")),
                    session.get("name"),
                    today
                )
            )


        # Save new weight
        else:

            connection.execute(
                """
                INSERT INTO weight_history (user_name, weight, date)
                VALUES (?, ?, ?)
                """,
                (
                    session.get("name"),
                    float(session.get("weight")),
                    today
                )
            )


        # Save database changes
        connection.commit()

        connection.close()


        return redirect(url_for("dashboard"))


    return render_template(
    "profile.html",
    name=session.get("name", ""),
    age=session.get("age", ""),
    gender=session.get("gender", ""),
    height=session.get("height", ""),
    weight=session.get("weight", ""),
    activity=session.get("activity", ""),
    food_preference=session.get("food_preference", ""),
    goal=session.get("goal", "")
)


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    bmi = None
    bmi_status = None
    calories = None
    water = None
    bmr = None

    try:

        height = float(session.get("height", 0))
        weight = float(session.get("weight", 0))
        age = int(session.get("age", 0))

        if height > 0 and weight > 0:

            height_m = height / 100

            # BMI Calculation
            bmi = round(weight / (height_m ** 2), 1)

            # BMI Status
            if bmi < 18.5:
                bmi_status = "Underweight"

            elif bmi < 25:
                bmi_status = "Normal"

            elif bmi < 30:
                bmi_status = "Overweight"

            else:
                bmi_status = "Obese"


            # Water Intake
            water = round(weight * 0.033, 1)


            # BMR Calculation
            gender = session.get("gender", "").lower()

            if gender == "male":

                bmr = round(
                    10 * weight
                    + 6.25 * height
                    - 5 * age
                    + 5
                )

            else:

                bmr = round(
                    10 * weight
                    + 6.25 * height
                    - 5 * age
                    - 161
                )


            # Activity Level
            activity = session.get("activity", "").lower()

            if activity == "low":
                calories = round(bmr * 1.2)

            elif activity == "moderate":
                calories = round(bmr * 1.55)

            elif activity == "high":
                calories = round(bmr * 1.725)

            else:
                calories = round(bmr * 1.3)


            # Health Goal
            goal = session.get("goal", "").lower()

            if "loss" in goal:
                calories -= 500

            elif "gain" in goal:
                calories += 300


    except:

        pass


    return render_template(
        "dashboard.html",
        name=session.get("name"),
        bmi=bmi,
        bmi_status=bmi_status,
        calories=calories,
        water=water,
        bmr=bmr
    )


# ---------------- DIET PLAN ----------------

@app.route("/diet-plan")
def diet_plan():

    goal = session.get("goal", "Healthy Lifestyle")
    food_preference = session.get("food_preference", "Vegetarian")

    diet = get_diet_plan(food_preference)

    return render_template(
        "diet_plan.html",
        goal=goal,
        food_preference=food_preference,
        diet=diet
    )


# ---------------- CHATBOT ----------------

@app.route("/chatbot")
def chatbot():

    return render_template("chatbot.html")


# ---------------- PROGRESS ----------------

# ---------------- PROGRESS ----------------

@app.route("/progress")
def progress():

    user_name = session.get("name")

    connection = get_db_connection()

    weight_history = connection.execute(
        """
        SELECT weight, date
        FROM weight_history
        WHERE user_name = ?
        ORDER BY date ASC
        """,
        (user_name,)
    ).fetchall()

    connection.close()


    # Agar abhi koi history available nahi hai
    if not weight_history:

        current_weight = float(
            session.get("weight", 0)
        )

        return render_template(
            "progress.html",
            weight=current_weight,
            weight_history=[],
            history_dates=[],
            history_weights=[]
        )


    # Database se latest weight
    current_weight = weight_history[-1]["weight"]


    # Date aur weight alag lists mein
    history_dates = [
        item["date"]
        for item in weight_history
    ]

    history_weights = [
        item["weight"]
        for item in weight_history
    ]


    return render_template(
        "progress.html",
        weight=current_weight,
        weight_history=weight_history,
        history_dates=history_dates,
        history_weights=history_weights
    )


# ---------------- ABOUT ----------------

@app.route("/about")
def about():

    return render_template("about.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app.run(debug=True)