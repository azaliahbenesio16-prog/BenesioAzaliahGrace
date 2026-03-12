from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# ----------------------------
# HTML UI
# ----------------------------
html = """
<!DOCTYPE html>
<html>
<head>
<title>Student Grade API</title>

<style>
body{
font-family: Arial;
background:#f0f2f5;
text-align:center;
}

.container{
width:650px;
margin:auto;
background:white;
padding:25px;
border-radius:10px;
box-shadow:0px 0px 10px gray;
}

input{
padding:10px;
margin:5px;
width:200px;
}

button{
padding:10px 15px;
margin:5px;
cursor:pointer;
background:#007bff;
color:white;
border:none;
border-radius:5px;
}

button:hover{
background:#0056b3;
}

.result{
margin-top:10px;
font-weight:bold;
}
</style>

</head>

<body>

<div class="container">

<h1>Flask Student Grade System</h1>

<hr>

<h3>Student Grade Calculator</h3>

<input type="text" id="name" placeholder="Student Name">
<input type="text" id="subject" placeholder="Subject">
<input type="number" id="score" placeholder="Score">

<br>

<button onclick="grade()">Calculate Grade</button>

<p id="gradeResult" class="result"></p>

<hr>

<h3>Calculator</h3>

<input type="number" id="num1" placeholder="First number">
<input type="number" id="num2" placeholder="Second number">

<br>

<button onclick="calc('add')">Add</button>
<button onclick="calc('subtract')">Subtract</button>
<button onclick="calc('multiply')">Multiply</button>
<button onclick="calc('divide')">Divide</button>

<p id="calcResult" class="result"></p>

<hr>

<h3>Hello API</h3>
<button onclick="hello()">Say Hello</button>
<p id="helloResult"></p>

<hr>

<h3>View API Routes</h3>
<button onclick="routes()">Show Routes</button>
<pre id="routesResult"></pre>

</div>

<script>

function grade(){

let name = document.getElementById("name").value
let subject = document.getElementById("subject").value
let score = document.getElementById("score").value

fetch("/grade/" + score + "/" + name + "/" + subject)
.then(res => res.json())
.then(data =>{

document.getElementById("gradeResult").innerText =
"Name: " + data.name +
" | Subject: " + data.subject +
" | Score: " + data.score +
" | Grade: " + data.grade +
" | Status: " + data.status

})

}

function calc(type){

let n1 = document.getElementById("num1").value
let n2 = document.getElementById("num2").value

fetch("/" + type + "/" + n1 + "/" + n2)
.then(res => res.json())
.then(data =>{
document.getElementById("calcResult").innerText =
"Result: " + data.result
})

}

function hello(){
fetch("/hello")
.then(res => res.json())
.then(data =>{
document.getElementById("helloResult").innerText = data.message
})
}

function routes(){
fetch("/routes")
.then(res => res.json())
.then(data =>{
document.getElementById("routesResult").innerText =
JSON.stringify(data, null, 2)
})
}

</script>

</body>
</html>
"""

# ----------------------------
# Home route
# ----------------------------
@app.route("/")
def home():
    return render_template_string(html)

# ----------------------------
# Hello route
# ----------------------------
@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from my API!"})

# ----------------------------
# Grade calculator with name and subject
# ----------------------------
@app.route("/grade/<int:score>/<name>/<subject>")
def grade(score, name, subject):

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
        "name": name,
        "subject": subject,
        "score": score,
        "grade": grade_letter,
        "status": status
    })

# ----------------------------
# Addition
# ----------------------------
@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    return jsonify({"result": num1 + num2})

# ----------------------------
# Subtraction
# ----------------------------
@app.route("/subtract/<int:num1>/<int:num2>")
def subtract(num1, num2):
    return jsonify({"result": num1 - num2})

# ----------------------------
# Multiplication
# ----------------------------
@app.route("/multiply/<int:num1>/<int:num2>")
def multiply(num1, num2):
    return jsonify({"result": num1 * num2})

# ----------------------------
# Division
# ----------------------------
@app.route("/divide/<int:num1>/<int:num2>")
def divide(num1, num2):

    if num2 == 0:
        return jsonify({"error": "Division by zero"}), 400

    return jsonify({"result": num1 / num2})

# ----------------------------
# Routes list
# ----------------------------
@app.route("/routes")
def routes():

    routes_table = [
        {"endpoint": "/", "description": "Main UI"},
        {"endpoint": "/hello", "description": "Hello message"},
        {"endpoint": "/grade/<score>/<name>/<subject>", "description": "Student grade calculator"},
        {"endpoint": "/add/<num1>/<num2>", "description": "Addition"},
        {"endpoint": "/subtract/<num1>/<num2>", "description": "Subtraction"},
        {"endpoint": "/multiply/<num1>/<num2>", "description": "Multiplication"},
        {"endpoint": "/divide/<num1>/<num2>", "description": "Division"}
    ]

    return jsonify(routes_table)

# ----------------------------
# Run Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
