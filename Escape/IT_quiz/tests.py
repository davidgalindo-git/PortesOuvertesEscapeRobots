import csv


def load_quiz(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def run_quiz(quiz_data):
    for q in quiz_data:
        print(f"\nQ{q['id']}: {q['question']}")
        print(f"A. {q['a']}")
        print(f"B. {q['b']}")
        print(f"C. {q['c']}")
        print(f"D. {q['d']}")
        answer = input("Your answer (a/b/c/d): ").strip().lower()
        if answer == q['correct']:
            print("✅ Correct!\n")
        else:
            print(f"❌ Wrong! The correct answer was {q['correct']}\n")


def main():
    print("Welcome to the Quiz App!")
    print("Choose a quiz:")
    print("1. IT Quiz")
    print("2. Cybersecurity Quiz")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        quiz = load_quiz("it_quiz.csv")
    elif choice == "2":
        quiz = load_quiz("cybersecurity_quiz.csv")
    else:
        print("Invalid choice.")
        return

    run_quiz(quiz)


if __name__ == "__main__":
    main()
