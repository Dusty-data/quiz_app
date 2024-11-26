import json
import time
from tools.encryption import encrypt, decrypt

# Load questions and answers
def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# User login or register
def login_or_register():
    users = load_json_file("users/users.json")
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    role = input("Are you a 'user' or 'teacher'? ").lower()
    user_id = f"{name}_{surname}".lower()
    
    if user_id in users:
        print(f"Welcome back, {users[user_id]['role'].capitalize()} {name}!")
        if users[user_id]["attempts"] >= 2:
            print("You have reached the maximum number of attempts.")
            exit()
    else:
        print("It seems you're new here. Let's register you!")
        role = input("Enter your role (teacher/student): ").strip().lower()
        if role not in ["teacher", "student"]:
            print("Invalid role. Please restart and enter a valid role.")
            exit()

        # Add the new user to the JSON file
        users[user_id] = {
            "name": name,
            "surname": surname,
            "role": role,
            "attempts": 0,
            "results": {}
        }
    
    save_json_file("users/users.json", users)
    print(f"Registration successful! Welcome, {role.capitalize()} {name}!")
    return user_id, users[user_id]

def main_menu(user_id, user_data):
    role = user_data["role"]

    if role == "teacher":
        print("\nTeacher Menu:")
        print("1. Manage questions for your section")
        print("2. View section statistics")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            manage_questions()
        elif choice == "2":
            view_section_statistics()
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Returning to menu...")
            main_menu(user_id, user_data)

    elif role == "student":
        print("\nStudent Menu:")
        print("1. Take the exam")
        print("2. View your results")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            overall_score = take_exam(user_id, user_data)
            if overall_score >= 75:
                print("Congratulations! You passed the exam.")
            else:
                print("Sorry, you did not pass the exam.")
        elif choice == "2":
            view_results(user_data)
        elif choice == "3":
            print("Exiting...")
            return
        else:
            print("Invalid choice. Returning to menu")
            main_menu(user_id, user_data)

    else:
        print("Invalid role. Exiting...")
        exit()

def main():
    user_id, user_data = login_or_register()
    main_menu(user_id, user_data)
    # Additional logic for handling menu choices will go here


# Show questions
def take_exam(user_id, user_data):
    sections = ["questions/questions_section1.json", "questions/questions_section2.json",
                "questions/questions_section3.json", "questions/questions_section4.json"]
    
    results = {}
    for i, section in enumerate(sections, start=1):
        print(f"\n--- Section {i} ---")
        questions = load_json_file(section)
        correct_answers = load_json_file("answers/answers.json")
        
        score = 0
        for q in questions:
            print(f"\n{q['question']}")
            for idx, opt in enumerate(q['options'], start=1):
                print(f"{idx}. {opt}")
            answer = input("Your answer: ")
            
            if answer in correct_answers[q['id']]:
                score += 1
        
        section_score = (score / len(questions)) * 100
        results[f"Section {i}"] = section_score
        print(f"Section {i} Score: {section_score:.2f}%")
    
    overall_score = sum(results.values()) / len(results)
    print(f"\nOverall Score: {overall_score:.2f}%")
    user_data["results"] = results
    user_data["attempts"] += 1
    return overall_score

def manage_questions():
    print("Manage questions for your section (placeholder).")
    # Add functionality here to allow teachers to add/edit/delete questions

def view_section_statistics():
    print("View section statistics (placeholder).")
    # Add functionality here to display statistics for the teacher's section

def view_results(user_data):
    """
    Displays the exam results for the logged-in student.
    """
    print("\nYour Exam Results:")
    if not user_data["results"]:
        print("No results found. Please take the exam first.")
        return

    for section, score in user_data["results"].items():
        print(f"{section}: {score:.2f}%")
    
    overall_score = sum(user_data["results"].values()) / len(user_data["results"])
    print(f"Overall Score: {overall_score:.2f}%")
    
    if overall_score >= 75:
        print("Status: Passed")
    else:
        print("Status: Failed")


# Main Program
def main():
    user_id, user_data = login_or_register()
    main_menu(user_id, user_data)
    print("\nStarting your exam...")
    overall_score = take_exam(user_id, user_data)
    
    if overall_score >= 75:
        print("Congratulations! You passed the exam.")
    else:
        print("Sorry, you did not pass the exam.")
    
    users = load_json_file("users/users.json")
    users[user_id] = user_data
    save_json_file("users/users.json", users)

if __name__ == "__main__":
    main()

