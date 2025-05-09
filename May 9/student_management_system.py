"""
Student Management System
- Demonstrates OOP concepts with classes, objects, methods, and attributes
- Implements functionality to add, remove, and search for students
- Takes input from the user for interactive operation
"""

class Student:
    """Class representing a student with basic information."""
    
    def __init__(self, student_id, name, age, grade):
        """Initialize a student with their details."""
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.courses = []
    
    def add_course(self, course):
        """Add a course to the student's course list."""
        if course not in self.courses:
            self.courses.append(course)
            return True
        return False
    
    def remove_course(self, course):
        """Remove a course from the student's course list."""
        if course in self.courses:
            self.courses.remove(course)
            return True
        return False
    
    def get_info(self):
        """Get a formatted string with student information."""
        info = f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"
        if self.courses:
            info += f", Courses: {', '.join(self.courses)}"
        return info


class StudentManagementSystem:
    """System to manage student records."""
    
    def __init__(self):
        """Initialize an empty student management system."""
        self.students = {}  # Dictionary to store students with ID as key
    
    def add_student(self, student):
        """Add a student to the system."""
        if student.student_id in self.students:
            return False
        
        self.students[student.student_id] = student
        return True
    
    def remove_student(self, student_id):
        """Remove a student from the system by ID."""
        if student_id in self.students:
            del self.students[student_id]
            return True
        
        return False
    
    def search_student(self, student_id):
        """Search for a student by ID."""
        if student_id in self.students:
            return self.students[student_id]
        
        return None
    
    def search_by_name(self, name):
        """Search for students by name (partial match)."""
        matching_students = []
        
        for student in self.students.values():
            if name.lower() in student.name.lower():
                matching_students.append(student)
        
        return matching_students
    
    def update_student_info(self, student_id, name=None, age=None, grade=None):
        """Update student information."""
        if student_id not in self.students:
            return False
        
        student = self.students[student_id]
        
        if name:
            student.name = name
        if age:
            student.age = age
        if grade:
            student.grade = grade
        
        return True
    
    def list_all_students(self):
        """List all students in the system."""
        return list(self.students.values())


def display_menu():
    """Display the main menu options."""
    print("\n===== Student Management System =====")
    print("1. Add a new student")
    print("2. Remove a student")
    print("3. Search for a student by ID")
    print("4. Search for students by name")
    print("5. Update student information")
    print("6. List all students")
    print("7. Manage student courses")
    print("8. Exit")
    print("====================================")


def display_course_menu():
    """Display the course management menu options."""
    print("\n===== Course Management =====")
    print("1. Add a course to a student")
    print("2. Remove a course from a student")
    print("3. Return to main menu")
    print("============================")


def get_valid_age():
    """Get a valid age input from the user."""
    while True:
        try:
            age = int(input("Enter student age: "))
            if age <= 0 or age > 100:
                print("Age must be between 1 and 100. Please try again.")
                continue
            return age
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Main program
if __name__ == "__main__":
    print("Welcome to the Student Management System!")
    sms = StudentManagementSystem()
    
    # Main menu loop
    while True:
        display_menu()
        
        try:
            choice = int(input("Enter your choice (1-8): "))
            
            if choice == 1:
                # Add a new student
                student_id = input("Enter student ID: ")
                
                # Check if student ID already exists
                if sms.search_student(student_id):
                    print(f"Error: Student with ID {student_id} already exists.")
                    continue
                
                name = input("Enter student name: ")
                
                try:
                    age = get_valid_age()
                except ValueError:
                    print("Invalid age. Student not added.")
                    continue
                
                grade = input("Enter student grade: ")
                
                # Create and add the student
                new_student = Student(student_id, name, age, grade)
                if sms.add_student(new_student):
                    print(f"Student {name} added successfully with ID: {student_id}")
                else:
                    print("Failed to add student.")
            
            elif choice == 2:
                # Remove a student
                student_id = input("Enter student ID to remove: ")
                
                # Find the student first to show their info
                student = sms.search_student(student_id)
                if student:
                    print(f"Found student: {student.get_info()}")
                    confirm = input("Are you sure you want to remove this student? (y/n): ").lower()
                    
                    if confirm == 'y':
                        if sms.remove_student(student_id):
                            print(f"Student with ID {student_id} removed successfully.")
                        else:
                            print(f"Failed to remove student with ID {student_id}.")
                    else:
                        print("Student removal cancelled.")
                else:
                    print(f"Student with ID {student_id} not found.")
            
            elif choice == 3:
                # Search for a student by ID
                student_id = input("Enter student ID to search: ")
                student = sms.search_student(student_id)
                
                if student:
                    print(f"Found student: {student.get_info()}")
                else:
                    print(f"Student with ID {student_id} not found.")
            
            elif choice == 4:
                # Search for students by name
                name = input("Enter student name to search (partial match allowed): ")
                matching_students = sms.search_by_name(name)
                
                if matching_students:
                    print(f"Found {len(matching_students)} matching students:")
                    for student in matching_students:
                        print(f"- {student.get_info()}")
                else:
                    print(f"No students found matching '{name}'.")
            
            elif choice == 5:
                # Update student information
                student_id = input("Enter student ID to update: ")
                student = sms.search_student(student_id)
                
                if student:
                    print(f"Current information: {student.get_info()}")
                    print("Enter new information (leave blank to keep current value):")
                    
                    name = input(f"Enter new name [{student.name}]: ")
                    
                    age_str = input(f"Enter new age [{student.age}]: ")
                    age = int(age_str) if age_str else None
                    
                    grade = input(f"Enter new grade [{student.grade}]: ")
                    
                    # Update with non-empty values
                    name = name if name else None
                    grade = grade if grade else None
                    
                    if sms.update_student_info(student_id, name, age, grade):
                        print("Student information updated successfully.")
                        print(f"New information: {student.get_info()}")
                    else:
                        print("Failed to update student information.")
                else:
                    print(f"Student with ID {student_id} not found.")
            
            elif choice == 6:
                # List all students
                students = sms.list_all_students()
                
                if students:
                    print(f"\nTotal students: {len(students)}")
                    print("All Students:")
                    for i, student in enumerate(students, 1):
                        print(f"{i}. {student.get_info()}")
                else:
                    print("No students in the system.")
            
            elif choice == 7:
                # Manage student courses
                student_id = input("Enter student ID: ")
                student = sms.search_student(student_id)
                
                if not student:
                    print(f"Student with ID {student_id} not found.")
                    continue
                
                print(f"Managing courses for student: {student.name}")
                
                while True:
                    display_course_menu()
                    
                    try:
                        course_choice = int(input("Enter your choice (1-3): "))
                        
                        if course_choice == 1:
                            # Add a course
                            course = input("Enter course name to add: ")
                            
                            if student.add_course(course):
                                print(f"Course '{course}' added for {student.name}.")
                            else:
                                print(f"Course '{course}' is already in {student.name}'s course list.")
                        
                        elif course_choice == 2:
                            # Remove a course
                            if not student.courses:
                                print(f"{student.name} is not enrolled in any courses.")
                                continue
                            
                            print(f"Current courses: {', '.join(student.courses)}")
                            course = input("Enter course name to remove: ")
                            
                            if student.remove_course(course):
                                print(f"Course '{course}' removed from {student.name}'s course list.")
                            else:
                                print(f"Course '{course}' not found in {student.name}'s course list.")
                        
                        elif course_choice == 3:
                            # Return to main menu
                            break
                        
                        else:
                            print("Invalid choice. Please enter a number between 1 and 3.")
                    
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            
            elif choice == 8:
                # Exit
                print("Thank you for using the Student Management System. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
