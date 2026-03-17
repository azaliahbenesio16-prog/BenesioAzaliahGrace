from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- HTML Template ---
html = """
<!DOCTYPE html>
<html>
<head>
<title>Student Grade System</title>
<style>
body{
font-family: Arial;
background:#f4f4f4;
text-align:center;
}
.container{
width:800px;
margin:auto;
background:white;
padding:20px;
border-radius:10px;
box-shadow:0px 0px 10px gray;
}
input{
padding:8px;
margin:5px;
}
button{
padding:8px 12px;
margin:5px;
cursor:pointer;
background:#007bff;
color:white;
border:none;
border-radius:5px;
}
table{
width:100%;
margin-top:20px;
border-collapse:collapse;
}
table, th, td{
border:1px solid gray;
padding:8px;
}
</style>
</head>
<body>
<div class="container">
<h1>Student Grade Management System</h1>
<h3>Add Student</h3>
<input id="name" placeholder="Student Name">
<input id="subject" placeholder="Subject">
<input id="score" type="number" placeholder="Score">
<input id="total" type="number" placeholder="Total Score">
<br>
<button onclick="addStudent()">Add Student</button>
<h3>Student List</h3>
<table>
<thead>
<tr>
<th>Name</th>
<th>Subject</th>
<th>Score</th>
<th>Percentage</th>
<th>Grade</th>
<th>Status</th>
<th>Action</th>
</tr>
</thead>
<tbody id="studentTable"></tbody>
</table>
</div>
<script>
function loadStudents(){
fetch("/students")
.then(res=>res.json())
.then(data=>{
let table=""
data.forEach((s,i)=>{
table+=`
<tr>
<td>${s.name}</td>
<td>${s.subject}</td>
<td>${s.score}/${s.total}</td>
<td>${s.percentage}%</td>
<td>${s.grade}</td>
<td>${s.status}</td>
<td>
<button onclick="deleteStudent(${s.id})">Delete</button>
</td>
</tr>
`
})
document.getElementById("studentTable").innerHTML=table
})
}
function addStudent(){
let name=document.getElementById("name").value
let subject=document.getElementById("subject").value
let score=document.getElementById("score").value
let total=document.getElementById("total").value
fetch("/add_student",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name,subject,score,total})
})
.then(res=>res.json())
.then(data=>{
document.getElementById("name").value=""
document.getElementById("subject").value=""
document.getElementById("score").value=""
document.getElementById("total").value=""
loadStudents()
})
}
function deleteStudent(id){
fetch("/delete_student/"+id,{
method:"DELETE"
})
.then(res=>res.json())
.then(data=>{
loadStudents()
})
}
loadStudents()
</script>
</body>
</html>
"""

# --- Routes ---
@app.route("/")
def home():
    return render_template_string(html)

@app.route("/students")
def get_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    
    students = []
    for s in data:
        students.append({
            "id": s[0],
            "name": s[1],
            "subject": s[2],
            "score": s[3],
            "total": s[4],
            "percentage": s[5],
            "grade": s[6],
            "status": s[7]
        })
    return jsonify(students)

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    name = data["name"]
    subject = data["subject"]
    score = int(data["score"])
    total = int(data["total"])
    
    percentage = (score / total) * 100
    if percentage >= 90:
        grade = "A"
    elif percentage >= 80:
        grade = "B"
    elif percentage >= 70:
        grade = "C"
    elif percentage >= 60:
        grade = "D"
    else:
        grade = "F"
    status = "Pass" if percentage >= 60 else "Fail"

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO students (name, subject, score, total, percentage, grade, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, subject, score, total, round(percentage, 2), grade, status))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student added"})

@app.route("/delete_student/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
