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
        print("Welcome back!")
        if users[user_id]["attempts"] >= 2:
            print("You have reached the maximum number of attempts.")
            exit()
    else:
        print("Registering new user...")
        users[user_id] = {"name": name, "surname": surname, "role": role, "attempts": 0, "results": {}}
    
    save_json_file("users/users.json", users)
    return user_id, users[user_id]

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

# Main Program
def main():
    user_id, user_data = login_or_register()
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

