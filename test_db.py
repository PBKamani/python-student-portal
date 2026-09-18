"""
Unit test script for database.py functionality:
- Database initialization
- Sample data seeding
- Fetch all students
- Search and filtering
- Analytics calculations
- Add student
- Update student
- Delete student
"""

import os
import database

def test_database():
    print("1. Testing DB initialization and seeding...")
    database.init_db()
    
    print("2. Testing get_all_students...")
    students = database.get_all_students()
    print(f"Total students loaded: {len(students)}")
    assert len(students) >= 12, "Expected at least 12 sample students"
    
    first = students[0]
    print(f"Sample student: {first['full_name']} ({first['student_id']}), Roll: {first['roll_no']}, Class: {first['class_name']}, Status: {first['status']}")

    print("3. Testing Search & Filtering...")
    search_res = database.get_all_students(search_query="Aarav")
    assert len(search_res) == 1, "Search by name failed"
    print(f"Search 'Aarav': found {search_res[0]['full_name']}")

    male_res = database.get_all_students(gender_filter="Male")
    female_res = database.get_all_students(gender_filter="Female")
    print(f"Gender filter: {len(male_res)} Males, {len(female_res)} Females")
    assert len(male_res) + len(female_res) == len(students)

    pass_res = database.get_all_students(status_filter="Pass")
    fail_res = database.get_all_students(status_filter="Fail")
    print(f"Status filter: {len(pass_res)} Passed, {len(fail_res)} Failed")

    print("4. Testing Analytics Calculation...")
    analytics = database.get_class_analytics()
    print("Analytics summary:")
    print(f" - Total Students: {analytics['total_students']}")
    print(f" - Present Today: {analytics['present_today']}")
    print(f" - Absent Today: {analytics['absent_today']}")
    print(f" - Class Avg Marks: {analytics['class_avg_marks']}%")
    print(f" - Pass Students: {analytics['pass_students']}")
    print(f" - Fail Students: {analytics['fail_students']}")
    print(f" - Favourite Subjects: {analytics['favourite_subjects']}")
    print(f" - Gender Distribution: {analytics['gender_distribution']}")
    print(f" - Subject Averages: {analytics['subject_averages']}")
    
    assert analytics['total_students'] == len(students)
    assert analytics['present_today'] + analytics['absent_today'] == analytics['total_students']
    assert analytics['pass_students'] + analytics['fail_students'] == analytics['total_students']
    
    print("5. Testing Add Student...")
    test_id = "STU-999"
    new_student = {
        "student_id": test_id,
        "full_name": "Test Student",
        "gender": "Female",
        "dob": "2009-03-25",
        "class_name": "Grade 10-A",
        "roll_no": 99,
        "email": "test@school.edu",
        "phone": "9998887776",
        "parent_name": "Parent Test",
        "parent_phone": "9998887775",
        "address": "Test Street",
        "favourite_subject": "Computer",
        "attendance_pct": 95.0
    }
    test_marks = {
        "Mathematics": 85.0,
        "Science": 90.0,
        "English": 88.0,
        "Computer": 92.0,
        "Social Science": 80.0
    }
    database.add_student(new_student, test_marks, today_status="Present")
    added = database.get_student(test_id)
    assert added is not None, "Failed to fetch newly added student"
    assert added["full_name"] == "Test Student"
    assert added["status"] == "Pass"
    print(f"Added successfully: {added['full_name']} with avg marks {added['average_marks']}%")

    print("6. Testing Update Student...")
    new_student["full_name"] = "Test Student Updated"
    test_marks["Mathematics"] = 99.0
    database.update_student(test_id, new_student, test_marks)
    updated = database.get_student(test_id)
    assert updated["full_name"] == "Test Student Updated"
    print(f"Updated successfully: {updated['full_name']}")

    print("7. Testing Delete Student...")
    database.delete_student(test_id)
    deleted = database.get_student(test_id)
    assert deleted is None, "Student was not deleted"
    print("Deleted successfully!")

    print("\nALL DATABASE AND ANALYTICS TESTS PASSED SUCCESSFULLY! [SUCCESS]")

if __name__ == "__main__":
    test_database()
