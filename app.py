from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    try:
        domain = request.form["domain"]
        fee = float(request.form["fee"])
        duration = float(request.form["duration"])
        level = request.form["level"]
        demand = request.form["demand"]

        # Domain scoring (expanded)
        domain_map = {
            "Web Development": 75,
            "Data Science": 88,
            "AI / ML": 92,
            "Finance": 80,
            "Commerce": 70,
            "Mathematics": 78,
            "Biology": 76,
            "Marketing": 77,
            "Cyber Security": 90,
            "UI/UX Design": 85
        }

        level_map = {
            "Student": 60,
            "Working Professional": 85
        }

        demand_map = {
            "Low": 50,
            "Medium": 75,
            "High": 95
        }

        # Feature engineering
        domain_score = domain_map.get(domain, 70)
        market_score = demand_map.get(demand, 70)
        experience_score = level_map.get(level, 60)
        cost_per_month = fee / duration

        X = np.array([[
            domain_score,
            market_score,
            experience_score,
            cost_per_month
        ]])

      # Manual weighted scoring system
        score = (
        domain_score * 0.30 +
        market_score * 0.30 +
        experience_score * 0.20 +
        (100 - min(cost_per_month, 100)) * 0.20
        )

        score = round(score / 100, 2) * 100

        # Balanced threshold
        status = "Worth It" if score >= 50 else "Not Worth It"

        # Breakdown
        breakdown = {
            "Domain Relevance": round(domain_score * 0.25, 2),
            "Market Demand": round(market_score * 0.30, 2),
            "Experience Level": round(experience_score * 0.15, 2),
            "Cost Efficiency": round((100 - min(cost_per_month, 100)) * 0.30, 2)
        }

        # Dynamic reasoning
        reasons = []

        if market_score >= 85:
            reasons.append("The selected domain has strong market demand.")
        elif market_score >= 70:
            reasons.append("The domain shows moderate demand in the job market.")
        else:
            reasons.append("The domain currently has lower market demand.")

        if experience_score >= 80:
            reasons.append("Your experience level aligns well with this course.")
        else:
            reasons.append("Your experience level may require additional preparation.")

        if cost_per_month <= 3000:
            reasons.append("The cost per month is affordable compared to duration.")
        elif cost_per_month <= 6000:
            reasons.append("The pricing is moderate and should be evaluated carefully.")
        else:
            reasons.append("The course appears expensive relative to its duration.")

        if score >= 50:
            conclusion = "Overall, this course is a worthwhile investment based on evaluated parameters."
        else:
            conclusion = "Overall, this course may not provide strong return on investment."

        return render_template(
            "result.html",
            score=score,
            status=status,
            breakdown=breakdown,
            domain=domain,
            reasons=reasons,
            conclusion=conclusion
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
