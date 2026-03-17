from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
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
html = """YOUR_EXISTING_HTML_HERE"""  # Replace with your HTML template from above

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
    
    # Convert to list of dicts
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
