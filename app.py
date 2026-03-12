from flask import Flask, jsonify

app = Flask(__name__)

# ----------------------------
# Home route
# ----------------------------
@app.route("/")
def home():
    return "Welcome to my Flask API!"

# ----------------------------
# Hello route
# ----------------------------
@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from my API!"})

# ----------------------------
# Grade calculator route
# ----------------------------
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

    status = "Pass" if score >= 60 else "Fail"

    return jsonify({
        "score": score,
        "grade": grade_letter,
        "status": status
    })

# ----------------------------
# Addition route
# ----------------------------
@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    result = num1 + num2
    return jsonify({
        "operation": "addition",
        "num1": num1,
        "num2": num2,
        "result": result
    })

# ----------------------------
# Subtraction route
# ----------------------------
@app.route("/subtract/<int:num1>/<int:num2>")
def subtract(num1, num2):
    result = num1 - num2
    return jsonify({
        "operation": "subtraction",
        "num1": num1,
        "num2": num2,
        "result": result
    })

# ----------------------------
# Multiplication route
# ----------------------------
@app.route("/multiply/<int:num1>/<int:num2>")
def multiply(num1, num2):
    result = num1 * num2
    return jsonify({
        "operation": "multiplication",
        "num1": num1,
        "num2": num2,
        "result": result
    })

# ----------------------------
# Division route
# ----------------------------
@app.route("/divide/<int:num1>/<int:num2>")
def divide(num1, num2):
    if num2 == 0:
        return jsonify({"error": "Division by zero is not allowed"}), 400
    result = num1 / num2
    return jsonify({
        "operation": "division",
        "num1": num1,
        "num2": num2,
        "result": result
    })

# ----------------------------
# Routes table route
# ----------------------------
@app.route("/routes")
def routes():
    """
    Returns a table of all endpoints, their description, and example usage.
    """
    routes_table = [
        {
            "endpoint": "/",
            "description": "Home route",
            "example": "/"
        },
        {
            "endpoint": "/hello",
            "description": "Returns a greeting message",
            "example": "/hello"
        },
        {
            "endpoint": "/grade/<score>",
            "description": "Returns grade letter and pass/fail status",
            "example": "/grade/85"
        },
        {
            "endpoint": "/add/<num1>/<num2>",
            "description": "Returns the sum of two numbers",
            "example": "/add/5/3"
        },
        {
            "endpoint": "/subtract/<num1>/<num2>",
            "description": "Returns the difference of two numbers",
            "example": "/subtract/10/4"
        },
        {
            "endpoint": "/multiply/<num1>/<num2>",
            "description": "Returns the product of two numbers",
            "example": "/multiply/6/7"
        },
        {
            "endpoint": "/divide/<num1>/<num2>",
            "description": "Returns the division of two numbers (handles division by zero)",
            "example": "/divide/10/2"
        }
    ]
    return jsonify({"routes": routes_table})

# ----------------------------
# Run the app
# ----------------------------
if __name__ == "__main__":
    app.run()
