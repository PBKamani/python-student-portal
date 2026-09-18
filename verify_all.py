"""
End-to-end simulation verification test for Student Management System.
Tests all requirements:
- Seeding & DB schema
- Analytics calculations & charts data contracts
- Search by name and ID
- Filters by gender and status
- Add Student CRUD flow
- Edit Student CRUD flow
- Delete Student CRUD flow
- Immediate KPI and Chart updates
"""

import sys
import database

def test_full_system():
    print("--- 1. Testing Initial State ---")
    database.init_db()
    students = database.get_all_students()
    print(f"Loaded {len(students)} students.")
    assert len(students) >= 12, "Should have at least 12 students."

    print("\n--- 2. Testing Class Analytics & Chart Data Sources ---")
    kpis = database.get_class_analytics()
    assert kpis["total_students"] == len(students)
    assert kpis["present_today"] + kpis["absent_today"] == kpis["total_students"]
    assert kpis["pass_students"] + kpis["fail_students"] == kpis["total_students"]
    assert len(kpis["favourite_subjects"]) > 0
    assert "Male" in kpis["gender_distribution"] and "Female" in kpis["gender_distribution"]
    assert len(kpis["marks_performance"]) == len(students)
    assert len(kpis["subject_averages"]) == 5
    assert len(kpis["attendance_comparison"]) == len(students)
    print("KPIs and Chart data sources verified:")
    print(f"  Total: {kpis['total_students']}, Present: {kpis['present_today']}, Absent: {kpis['absent_today']}, Avg: {kpis['class_avg_marks']}%")

    print("\n--- 3. Testing Search & Filtering ---")
    # Search by Name
    res_name = database.get_all_students(search_query="Ananya")
    assert len(res_name) == 1 and res_name[0]["student_id"] == "STU-102"
    # Search by ID
    res_id = database.get_all_students(search_query="STU-105")
    assert len(res_id) == 1 and res_id[0]["full_name"] == "Kabir Shah"
    # Filter by Gender
    males = database.get_all_students(gender_filter="Male")
    females = database.get_all_students(gender_filter="Female")
    assert len(males) + len(females) == len(students)
    # Filter by Pass/Fail
    pass_list = database.get_all_students(status_filter="Pass")
    fail_list = database.get_all_students(status_filter="Fail")
    assert len(pass_list) + len(fail_list) == len(students)
    print("Search and Filter assertions passed.")

    print("\n--- 4. Testing CRUD: Add Student ---")
    initial_total = kpis["total_students"]
    test_id = "STU-TEST-01"
    new_data = {
        "student_id": test_id,
        "full_name": "Test Candidate",
        "gender": "Female",
        "dob": "2009-06-15",
        "class_name": "Grade 10-A",
        "roll_no": 99,
        "email": "test.candidate@school.edu",
        "phone": "9800000001",
        "parent_name": "Parent Candidate",
        "parent_phone": "9800000002",
        "address": "404 Test Way",
        "favourite_subject": "Computer",
        "attendance_pct": 92.0
    }
    marks = {
        "Mathematics": 95.0,
        "Science": 90.0,
        "English": 88.0,
        "Computer": 98.0,
        "Social Science": 89.0
    }
    database.add_student(new_data, marks, today_status="Present")
    
    # Verify addition
    added_stu = database.get_student(test_id)
    assert added_stu is not None
    assert added_stu["full_name"] == "Test Candidate"
    assert added_stu["status"] == "Pass"
    assert added_stu["average_marks"] == 92.0

    # Verify real-time metrics update
    kpis_after_add = database.get_class_analytics()
    assert kpis_after_add["total_students"] == initial_total + 1
    assert kpis_after_add["present_today"] == kpis["present_today"] + 1
    print("Add Student passed and metrics updated immediately.")

    print("\n--- 5. Testing CRUD: Edit Student ---")
    new_data["full_name"] = "Test Candidate Updated"
    # Change marks to fail
    failing_marks = {
        "Mathematics": 25.0,
        "Science": 30.0,
        "English": 20.0,
        "Computer": 35.0,
        "Social Science": 28.0
    }
    database.update_student(test_id, new_data, failing_marks)
    updated_stu = database.get_student(test_id)
    assert updated_stu["full_name"] == "Test Candidate Updated"
    assert updated_stu["status"] == "Fail"
    assert updated_stu["average_marks"] == 27.6
    print("Edit Student passed and recalculated pass/fail status.")

    print("\n--- 6. Testing CRUD: Delete Student ---")
    database.delete_student(test_id)
    assert database.get_student(test_id) is None
    kpis_after_del = database.get_class_analytics()
    assert kpis_after_del["total_students"] == initial_total
    print("Delete Student passed and restored metrics.")

    print("\n==========================================")
    print("ALL 19 AUDIT CHECKS COMPLETED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    test_full_system()
