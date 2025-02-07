from flask import Flask, request, jsonify
import threading

class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}, Age: {self.age}"

class StudentManagementSystem:
    def __init__(self):
        self.app = Flask(__name__)
        self.students = []

        @self.app.route('/students', methods=['GET'])
        def get_students():
            return jsonify([str(student) for student in self.students])

        @self.app.route('/students', methods=['POST'])
        def add_student():
            data = request.json
            if 'name' in data and 'age' in data and 'student_id' in data:
                student = Student(data['name'], data['age'], data['student_id'])
                self.students.append(student)
                return jsonify({"message": f"Student {student.name} added successfully."}), 201
            return jsonify({"error": "Invalid data format"}), 400

        @self.app.route('/students/<student_id>', methods=['DELETE'])
        def remove_student(student_id):
            for student in self.students:
                if student.student_id == student_id:
                    self.students.remove(student)
                    return jsonify({"message": f"Student ID {student_id} removed successfully."}), 200
            return jsonify({"message": f"Student ID {student_id} not found."}), 404

    def run_server(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

    def add_student(self, student):
        self.students.append(student)
        print(f"Student {student.name} added successfully.")

    def remove_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print(f"Student ID {student_id} removed successfully.")
                return
        print(f"Student ID {student_id} not found.")

    def display_students(self):
        if not self.students:
            print("No students in the system.")
        else:
            for student in self.students:
                print(student)

# Create the StudentManagementSystem instance
sms = StudentManagementSystem()

# Run Flask server in a separate thread
server_thread = threading.Thread(target=sms.run_server, daemon=True)
server_thread.start()

# CLI Interface (Runs in Main Thread)
def cli_interface():
    while True:
        print("\n1. Add Student")
        print("2. Remove Student")
        print("3. Display Students")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            age = input("Enter student age: ")
            student_id = input("Enter student ID: ")
            student = Student(name, age, student_id)
            sms.add_student(student)
        elif choice == '2':
            student_id = input("Enter student ID to remove: ")
            sms.remove_student(student_id)
        elif choice == '3':
            sms.display_students()
        elif choice == '4':
            print("Exiting CLI...")
            break
        else:
            print("Invalid choice. Please try again.")

cli_interface()
