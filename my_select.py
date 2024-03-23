from sqlalchemy import func
from models import Student, Grade, Subject, Lecturer, Group
from db_session import session


QUERIES = {
    1: "Znajdź 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.",
    2: "Znajdź ucznia z najwyższą średnią ocen z wybranego przedmiotu.",
    3: "Znajdź średni wynik w grupach dla wybranego przedmiotu.",
    4: "Znajdź średni wynik w grupie (w całej tabeli ocen).",
    5: "Znajdź przedmioty, które prowadzi wybrany wykładowca.",
    6: "Znajdź listę uczniów w wybranej grupie.",
    7: "Znajdź oceny uczniów w wybranej grupie z określonego przedmiotu.",
    8: "Znajdź średnią ocen wystawioną przez wykładowcę z danego przedmiotu.",
    9: "Znajdź listę kursów, na które uczęszcza uczeń.",
    10: "Znajdź listę kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia.",
}

# Zapytanie 1: Znajdź 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.
def select_1():
    top_students = session.query(Grade.student_id, func.avg(Grade.grade).label('average_grade'))\
                          .group_by(Grade.student_id)\
                          .order_by(func.avg(Grade.grade).desc())\
                          .limit(5).all()
    return top_students

# Zapytanie 2: Znajdź ucznia z najwyższą średnią ocen z wybranego przedmiotu.
def select_2(subject_id):
    top_student = session.query(Grade.student_id, func.avg(Grade.grade).label('average_grade'))\
                        .filter(Grade.subject_id == subject_id)\
                        .group_by(Grade.student_id)\
                        .order_by(func.avg(Grade.grade).desc())\
                        .first()
    return top_student

# Zapytanie 3: Znajdź średni wynik w grupach dla wybranego przedmiotu.
def select_3(subject_id):
    average_grades_per_group = session.query(Student.group_id, func.avg(Grade.grade).label('average_grade'))\
                                      .join(Grade, Student.id == Grade.student_id)\
                                      .filter(Grade.subject_id == subject_id)\
                                      .group_by(Student.group_id).all()
    return average_grades_per_group

# Zapytanie 4: Znajdź średni wynik w grupie (w całej tabeli ocen).
def select_4():
    average_grades_per_group = session.query(Student.group_id, func.avg(Grade.grade).label('average_grade'))\
                                      .join(Grade, Student.id == Grade.student_id)\
                                      .group_by(Student.group_id).all()
    return average_grades_per_group

# Zapytanie 5: Znajdź przedmioty, które prowadzi wybrany wykładowca.
def select_5(lecturer_id):
    subjects_taught = session.query(Subject.subject_name)\
                             .filter(Subject.lecturer_id == lecturer_id).all()
    return subjects_taught

# Zapytanie 6: Znajdź listę uczniów w wybranej grupie.
def select_6(group_id):
    students_in_group = session.query(Student.student_name)\
                               .filter(Student.group_id == group_id).all()
    return students_in_group

# Zapytanie 7: Znajdź oceny uczniów w wybranej grupie z określonego przedmiotu.
def select_7(group_id, subject_id):
    grades_in_group = session.query(Student.student_name, Grade.grade)\
                             .join(Grade, Student.id == Grade.student_id)\
                             .filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return grades_in_group

# Zapytanie 8: Znajdź średnią ocenę wystawioną przez wykładowcę z danego przedmiotu.
def select_8(lecturer_id, subject_id):
    average_grade_by_lecturer = session.query(func.avg(Grade.grade).label('average_grade'))\
                                        .join(Subject, Subject.id == Grade.subject_id)\
                                        .filter(Subject.lecturer_id == lecturer_id, Subject.id == subject_id).first()
    return average_grade_by_lecturer

# Zapytanie 9: Znajdź listę przedmiotów zaliczonych przez danego studenta.
def select_9(student_id):
    passed_subjects = session.query(Subject.subject_name)\
                             .join(Grade, Subject.id == Grade.subject_id)\
                             .filter(Grade.student_id == student_id).all()
    return passed_subjects

# Zapytanie 10: Znajdź listę kursów prowadzonych przez wybranego wykładowcę dla określonego studenta.
def select_10(student_id, lecturer_id):
    courses_taken_by_student = session.query(Subject.subject_name)\
                                      .join(Grade, Subject.id == Grade.subject_id)\
                                      .filter(Subject.lecturer_id == lecturer_id, Grade.student_id == student_id).all()
    return courses_taken_by_student

if __name__ == '__main__':
    # Wywołanie funkcji i wydrukowanie wyników
    for query_num, query_text in QUERIES.items():
        print(f"Zadanie {query_num}: {query_text}")
        if query_num == 1:
            result = select_1()
            for student_id, average_grade in result:
                print(student_id, float(average_grade))
            print(f"\n")
        elif query_num == 2:
            result = select_2(1)
            if result:
                print(result[0], float(result[1]))
            else:
                print("Brak danych")
            print(f"\n")
        elif query_num == 3:
            result = select_3(1)
            for group_id, average_grade in result:
                print(group_id, float(average_grade))
            print(f"\n")
        elif query_num == 4:
            result = select_4()
            for group_id, average_grade in result:
                print(group_id, float(average_grade))
            print(f"\n")
        elif query_num == 5:
            result = select_5(1) 
            print(result) 
            print(f"\n")
        elif query_num == 6:
            result = select_6(1)  
            for student_name, in result:
                print(student_name)
            print(f"\n")
        elif query_num == 7:
            result = select_7(1, 1) 
            for student_name, grade in result:
                print(student_name, grade)
            print(f"\n")
        elif query_num == 8:
            result = select_8(1, 3) 
            print(float(result[0])) 
            print(f"\n")
        elif query_num == 9:
            result = select_9(1)  
            print(result) 
            print(f"\n")
        elif query_num == 10:
            result = select_10(1, 1)  
            print(result)  
