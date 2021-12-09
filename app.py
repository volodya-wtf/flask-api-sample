from flask import Flask
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("students.sqlite")
    except sqlite3.error as e:
        print(e)
    return e


@app.route("/students", methods=["POST", "GET"])
def students():
    conn = db_connection()
    cursor = conn.cursor()


@app.route('/student/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def student(id):
    conn = db_connection()
    cursor = conn.cursor()
    student = None


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
