import matplotlib.pyplot as plt
import os



# Load students into dict: {id: name}
def load_students(path='data/students.txt'):
    students = {}
    with open(path, 'r') as file:
        for line in file:
            id_ = line[:3]
            name = line[3:].strip()
            students[id_] = name
    return students


# Load assignments into dicts
def load_assignments(path='data/assignments.txt'):
    assignments = {}
    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id_ = lines[i + 1].strip()
            points = int(lines[i + 2].strip())
            assignments[id_] = {'name': name, 'points': points}
    return assignments


# Load all submissions
def load_submissions(path='data/submissions'):
    submissions = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            with open(os.path.join(path, filename), 'r') as file:
                for line in file:
                    student_id, assignment_id, percent = line.strip().split('|')
                    submissions.append((student_id, assignment_id, float(percent)))
    return submissions


# Menu Option 1: Student grade
def calculate_student_grade(name, students, assignments, submissions):
    for id_, student_name in students.items():
        if student_name.lower() == name.lower():
            total_earned = 0
            for sid, aid, percent in submissions:
                if sid == id_:
                    total_earned += (percent / 100) * assignments[aid]['points']
            print(f"{round((total_earned / 1000) * 100)}%")
            return
    print("Student not found")


# Menu Option 2: Assignment stats
def assignment_statistics(name, assignments, submissions):
    ids = [aid for aid, info in assignments.items() if info['name'].lower() == name.lower()]
    if not ids:
        print("Assignment not found")
        return
    aid = ids[0]
    scores = [percent for _, a_id, percent in submissions if a_id == aid]
    if scores:
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")
        print(f"Max: {int(max(scores))}%")


# Menu Option 3: Graph
def assignment_graph(name, assignments, submissions):
    ids = [aid for aid, info in assignments.items() if info['name'].lower() == name.lower()]
    if not ids:
        print("Assignment not found")
        return
    aid = ids[0]
    scores = [percent for _, a_id, percent in submissions if a_id == aid]
    if scores:
        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f"Scores for {name}")
        plt.xlabel("Score (%)")
        plt.ylabel("Number of Students")
        plt.show()


# Main
def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph")
    choice = input("Enter your selection: ")

    if choice == '1':
        name = input("What is the student's name: ")
        calculate_student_grade(name, students, assignments, submissions)
    elif choice == '2':
        name = input("What is the assignment name: ")
        assignment_statistics(name, assignments, submissions)
    elif choice == '3':
        name = input("What is the assignment name: ")
        assignment_graph(name, assignments, submissions)


if __name__ == "__main__":
    main()
