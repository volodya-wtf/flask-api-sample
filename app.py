from flask import Flask
from flask import jsonify
from flask import request

import sqlite3


app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("students.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/students", methods=["POST", "GET"])
def students():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM students")
        students = [
            dict(id=row[0], firstname=row[1], lastname=row[2], telegram=row[4])
            for row in cursor.fetchall()
        ]
        if students is not None:
            return jsonify(students)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        telegram = request.form["telegram"]

        sql = """INSERT INTO students (firstname, lastname, telegram)
        VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (firstname, lastname, telegram))
        conn.commit()

        return f"Student with id: {cursor.lastrowid} created successfully"


@app.route("/student/<int:id>", methods=["GET", "PUT", "DELETE"])
def student(id):
    conn = db_connection()
    cursor = conn.cursor()
    student = None

    if request.method == "GET":
        cursor.execute("SELECT * FROM students WHERE id=?", (id,))
        rows = cursor.fetchall()
        for row in rows:
            student = row
        if student is not None:
            return jsonify(student), 200
        else:
            return "Something went wrong", 404

    if request.method == "PUT":
        sql = """UPDATE students SET firstname = ?, lastname = ?, telegram = ? WHERE id = ?"""

        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        telegram = request.form["telegram"]
        updated_student = {
            "id": id,
            "firstname": firstname,
            "lastname": lastname,
        }

        conn.execute(sql, (firstname, lastname, telegram, id))
        conn.commit()

        return jsonify(updated_student)

    if request.method == "DELETE":
        sql = """ DELETE FROM students WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()

        return f"Student with id: {id} has been deleted.", 200


if __name__ == "__main__":
    app.run(debug=True)


# >>> import sqlite3
# >>> conn = sqlite3.connect("students.sqlite")
# >>> cursor = conn.cursor()
# >>> sql_query = """ CREATE TABLE students (
# ...     id INTEGER PRIMARY KEY,
# ...     firstname TEXT NOT NULL,
# ...     lastname TEXT NOT NULL,
# ...     telegram TEXT NOT NULL
# ... )"""
# >>> cursor.execute(sql_query)
