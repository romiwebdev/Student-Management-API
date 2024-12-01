import os
from flask import Flask, request, jsonify, make_response, Blueprint

app = Flask(__name__)

# Simulasi database
students = [
    {"id": 1, "nama": "Romi", "kelas": "XII-3"},
    {"id": 2, "nama": "Dina", "kelas": "XII-2"},
]

# Blueprint untuk modularisasi
api_bp = Blueprint("api", __name__)

# Root endpoint
@app.route("/", methods=["GET"])
def root():
    return "Welcome to the Flask App!"

# About endpoint
@app.route("/about", methods=["GET"])
def about():
    return make_response(jsonify({"nama": "Romi", "kelas": "XII-3"}))

# Endpoint untuk mendapatkan semua siswa
@api_bp.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200

# Endpoint untuk menambahkan siswa baru
@api_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    if not data or "nama" not in data or "kelas" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_student = {
        "id": len(students) + 1,
        "nama": data["nama"],
        "kelas": data["kelas"],
    }
    students.append(new_student)
    return jsonify({"message": "Student added successfully", "student": new_student}), 201

# Endpoint dinamis untuk mendapatkan siswa berdasarkan ID
@api_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200

# Endpoint untuk upload file
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filepath": filepath}), 201

# Error handler untuk 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Register blueprint
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    # Pastikan folder uploads ada
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
