from flask import Flask

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Welcome to my Flask API!"

# Hello route
@app.route("/hello")
def hello():
    return "Hello from my API!"

# Updated grade endpoint
@app.route("/grade/<int:score>")
def grade(score):
    if score >= 90:
        grade_letter = "A"
    elif score >= 80:
        grade_letter = "B"
    elif score >= 70:
        grade_letter = "C"
    elif score >= 60:
        grade_letter = "D"
    else:
        grade_letter = "F"

    return {
        "score": score,
        "grade": grade_letter,
        "status": "Pass" if score >= 60 else "Fail"
    }

# Addition endpoint
@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    return {
        "num1": num1,
        "num2": num2,
        "result": num1 + num2
    }

if __name__ == "__main__":
    app.run()
