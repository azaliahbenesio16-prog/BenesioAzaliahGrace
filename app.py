from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

students = []

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

<tbody id="studentTable">
</tbody>

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
<button onclick="deleteStudent(${i})">Delete</button>
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

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/students")
def get_students():
    return jsonify(students)

@app.route("/add_student", methods=["POST"])
def add_student():

    data=request.json

    name=data["name"]
    subject=data["subject"]
    score=int(data["score"])
    total=int(data["total"])

    percentage=(score/total)*100

    if percentage>=90:
        grade="A"
    elif percentage>=80:
        grade="B"
    elif percentage>=70:
        grade="C"
    elif percentage>=60:
        grade="D"
    else:
        grade="F"

    status="Pass" if percentage>=60 else "Fail"

    student={
        "name":name,
        "subject":subject,
        "score":score,
        "total":total,
        "percentage":round(percentage,2),
        "grade":grade,
        "status":status
    }

    students.append(student)

    return jsonify({"message":"Student added"})

@app.route("/delete_student/<int:id>", methods=["DELETE"])
def delete_student(id):

    students.pop(id)

    return jsonify({"message":"Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
