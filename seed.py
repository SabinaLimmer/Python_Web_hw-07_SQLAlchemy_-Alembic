from faker import Faker
from random import randint, choice
from models import Student, Group, Lecturer, Subject, Grade
from db_session import session

NUMBER_STUDENTS = 30
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 5
NUMBER_LECTURERS = 3
GRADES_SCOPE = [2, 3, 4, 5]
SUBJECTS_NAMES = ["Math", "Physics", "Chemistry", "Biology", "History"]

def generate_fake_data(number_students, number_groups, number_subjects, number_lecturers, grades_scope, subjects_names):
    fake = Faker()

    fake_students = [(fake.name(), randint(1, number_groups)) for _ in range(number_students)]
    fake_groups = [(i,) for i in range(1, number_groups + 1)]
    fake_lecturers = [(fake.name(),) for _ in range(number_lecturers)]
    fake_subjects = [(name, randint(1, number_lecturers)) for name in subjects_names]

    fake_grades = []
    for student_id in range(1, number_students + 1):
        for _ in range(randint(15, 20)):
            grade_date = fake.date_between(start_date="-1y", end_date="today")
            fake_grades.append({
                "grade": choice(grades_scope),
                "date_of": grade_date,
                "subject_id": randint(1, number_subjects),
                "student_id": student_id
            })

    return fake_students, fake_groups, fake_lecturers, fake_subjects, fake_grades

def seed_database():

    students, groups, lecturers, subjects, grades = generate_fake_data(NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_SUBJECTS, NUMBER_LECTURERS, GRADES_SCOPE, SUBJECTS_NAMES)

    for group in groups:
        session.add(Group(group_number=group[0]))

    for lecturer in lecturers:
        session.add(Lecturer(lecturer_name=lecturer[0]))

    for subject in subjects:
        session.add(Subject(subject_name=subject[0], lecturer_id=subject[1]))

    for student in students:
        session.add(Student(student_name=student[0], group_id=student[1]))

    for grade in grades:
        session.add(Grade(grade=grade["grade"], date_of=grade["date_of"], subject_id=grade["subject_id"], student_id=grade["student_id"]))

    session.commit()


if __name__ == "__main__":
    seed_database()
