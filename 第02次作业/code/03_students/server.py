from pathlib import Path
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False
DB_PATH = Path(__file__).resolve().parent / "students.db"


@app.route("/", methods=["GET", "POST"])
def process():
    opt = request.values.get("opt", "")

    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row

            if opt == "init":
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        No TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Sex TEXT NOT NULL,
                        Age INTEGER NOT NULL
                    )
                """)
                return jsonify(msg="OK")

            if opt == "insert":
                no = request.form.get("No", "").strip()
                name = request.form.get("Name", "").strip()
                sex = request.form.get("Sex", "")
                age = int(request.form.get("Age", ""))

                if not no or not name or sex not in ("男", "女"):
                    return jsonify(msg="学生信息不完整"), 400
                if not 0 <= age <= 120:
                    return jsonify(msg="年龄无效"), 400

                connection.execute(
                    "INSERT INTO students (No, Name, Sex, Age) VALUES (?, ?, ?, ?)",
                    (no, name, sex, age),
                )
                return jsonify(msg="OK")

            if opt == "delete":
                no = request.form.get("No", "").strip()
                cursor = connection.execute(
                    "DELETE FROM students WHERE No = ?", (no,)
                )
                if cursor.rowcount == 0:
                    return jsonify(msg="学号不存在"), 404
                return jsonify(msg="OK")

            if opt == "":
                rows = connection.execute(
                    "SELECT No, Name, Sex, Age FROM students ORDER BY No"
                ).fetchall()
                return jsonify(msg="OK", data=[dict(row) for row in rows])

            return jsonify(msg="操作无效"), 400

    except sqlite3.IntegrityError:
        return jsonify(msg="学号已存在"), 409
    except ValueError:
        return jsonify(msg="年龄必须是整数"), 400
    except sqlite3.Error as error:
        return jsonify(msg=str(error)), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
