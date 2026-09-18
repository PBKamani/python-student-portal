"""
Database management module for Student Management System.
Uses SQLite for persistent, lightweight local storage.
"""

import sqlite3
import os
from datetime import date, datetime
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "school.db")
SUBJECTS = ["Mathematics", "Science", "English", "Computer", "Social Science"]


def get_connection():
    """Create and return a database connection with row factory configured."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initialize database tables and seed sample data if empty."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                dob TEXT NOT NULL,
                class_name TEXT NOT NULL,
                roll_no INTEGER NOT NULL,
                email TEXT,
                phone TEXT,
                parent_name TEXT,
                parent_phone TEXT,
                address TEXT,
                favourite_subject TEXT,
                attendance_pct REAL DEFAULT 0.0,
                average_marks REAL DEFAULT 0.0,
                status TEXT DEFAULT 'Pass',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Subject marks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
        """)
        
        # Daily attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                UNIQUE(student_id, date)
            )
        """)
        
        conn.commit()

        # Check if students exist, if not seed sample data
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        if count == 0:
            seed_sample_data(conn)


def seed_sample_data(conn: sqlite3.Connection):
    """Seed 12 realistic sample students with marks, today's attendance, and analytics."""
    sample_students = [
        {
            "student_id": "STU-101",
            "full_name": "Aarav Patel",
            "gender": "Male",
            "dob": "2009-04-12",
            "class_name": "Grade 10-A",
            "roll_no": 1,
            "email": "aarav.patel@school.edu",
            "phone": "9876543210",
            "parent_name": "Ramesh Patel",
            "parent_phone": "9876543211",
            "address": "12 Shanti Nagar, Surat",
            "favourite_subject": "Mathematics",
            "attendance_pct": 94.0,
            "marks": {"Mathematics": 95, "Science": 92, "English": 88, "Computer": 96, "Social Science": 84},
            "today_status": "Present"
        },
        {
            "student_id": "STU-102",
            "full_name": "Ananya Sharma",
            "gender": "Female",
            "dob": "2009-08-25",
            "class_name": "Grade 10-A",
            "roll_no": 2,
            "email": "ananya.sharma@school.edu",
            "phone": "9823456781",
            "parent_name": "Vikram Sharma",
            "parent_phone": "9823456780",
            "address": "45 Green Park, Ahmedabad",
            "favourite_subject": "Science",
            "attendance_pct": 98.0,
            "marks": {"Mathematics": 90, "Science": 96, "English": 94, "Computer": 92, "Social Science": 90},
            "today_status": "Present"
        },
        {
            "student_id": "STU-103",
            "full_name": "Rohan Mehta",
            "gender": "Male",
            "dob": "2009-02-14",
            "class_name": "Grade 10-A",
            "roll_no": 3,
            "email": "rohan.mehta@school.edu",
            "phone": "9812345678",
            "parent_name": "Sanjay Mehta",
            "parent_phone": "9812345679",
            "address": "8 Lotus Court, Bardoli",
            "favourite_subject": "Computer",
            "attendance_pct": 86.0,
            "marks": {"Mathematics": 78, "Science": 74, "English": 70, "Computer": 88, "Social Science": 68},
            "today_status": "Present"
        },
        {
            "student_id": "STU-104",
            "full_name": "Diya Joshi",
            "gender": "Female",
            "dob": "2009-11-03",
            "class_name": "Grade 10-A",
            "roll_no": 4,
            "email": "diya.joshi@school.edu",
            "phone": "9723456123",
            "parent_name": "Mahesh Joshi",
            "parent_phone": "9723456124",
            "address": "102 Sunrise Apts, Navsari",
            "favourite_subject": "English",
            "attendance_pct": 91.0,
            "marks": {"Mathematics": 82, "Science": 85, "English": 96, "Computer": 80, "Social Science": 88},
            "today_status": "Present"
        },
        {
            "student_id": "STU-105",
            "full_name": "Kabir Shah",
            "gender": "Male",
            "dob": "2009-06-18",
            "class_name": "Grade 10-A",
            "roll_no": 5,
            "email": "kabir.shah@school.edu",
            "phone": "9834567890",
            "parent_name": "Hemant Shah",
            "parent_phone": "9834567891",
            "address": "22 Riverview, Surat",
            "favourite_subject": "Mathematics",
            "attendance_pct": 68.0,
            "marks": {"Mathematics": 38, "Science": 34, "English": 42, "Computer": 35, "Social Science": 36},
            "today_status": "Absent"
        },
        {
            "student_id": "STU-106",
            "full_name": "Pooja Trivedi",
            "gender": "Female",
            "dob": "2009-09-30",
            "class_name": "Grade 10-A",
            "roll_no": 6,
            "email": "pooja.trivedi@school.edu",
            "phone": "9745678901",
            "parent_name": "Kishore Trivedi",
            "parent_phone": "9745678902",
            "address": "5 Vasundhara, Bardoli",
            "favourite_subject": "Social Science",
            "attendance_pct": 89.0,
            "marks": {"Mathematics": 72, "Science": 76, "English": 84, "Computer": 75, "Social Science": 92},
            "today_status": "Present"
        },
        {
            "student_id": "STU-107",
            "full_name": "Dev Desai",
            "gender": "Male",
            "dob": "2009-01-20",
            "class_name": "Grade 10-A",
            "roll_no": 7,
            "email": "dev.desai@school.edu",
            "phone": "9856789012",
            "parent_name": "Bhavesh Desai",
            "parent_phone": "9856789013",
            "address": "17 Orchid Enclave, Surat",
            "favourite_subject": "Computer",
            "attendance_pct": 95.0,
            "marks": {"Mathematics": 88, "Science": 90, "English": 82, "Computer": 98, "Social Science": 80},
            "today_status": "Present"
        },
        {
            "student_id": "STU-108",
            "full_name": "Isha Verma",
            "gender": "Female",
            "dob": "2009-05-15",
            "class_name": "Grade 10-A",
            "roll_no": 8,
            "email": "isha.verma@school.edu",
            "phone": "9867890123",
            "parent_name": "Rajeev Verma",
            "parent_phone": "9867890124",
            "address": "33 Royal Heights, Surat",
            "favourite_subject": "Science",
            "attendance_pct": 92.0,
            "marks": {"Mathematics": 85, "Science": 94, "English": 89, "Computer": 86, "Social Science": 87},
            "today_status": "Present"
        },
        {
            "student_id": "STU-109",
            "full_name": "Manish Chauhan",
            "gender": "Male",
            "dob": "2009-12-08",
            "class_name": "Grade 10-A",
            "roll_no": 9,
            "email": "manish.c@school.edu",
            "phone": "9878901234",
            "parent_name": "Ashok Chauhan",
            "parent_phone": "9878901235",
            "address": "9 Gandhi Path, Navsari",
            "favourite_subject": "Mathematics",
            "attendance_pct": 58.0,
            "marks": {"Mathematics": 32, "Science": 28, "English": 35, "Computer": 40, "Social Science": 30},
            "today_status": "Absent"
        },
        {
            "student_id": "STU-110",
            "full_name": "Kavya Nair",
            "gender": "Female",
            "dob": "2009-07-22",
            "class_name": "Grade 10-A",
            "roll_no": 10,
            "email": "kavya.nair@school.edu",
            "phone": "9889012345",
            "parent_name": "Pradeep Nair",
            "parent_phone": "9889012346",
            "address": "60 Palm Residency, Surat",
            "favourite_subject": "English",
            "attendance_pct": 96.0,
            "marks": {"Mathematics": 79, "Science": 83, "English": 95, "Computer": 84, "Social Science": 86},
            "today_status": "Present"
        },
        {
            "student_id": "STU-111",
            "full_name": "Vivek Rana",
            "gender": "Male",
            "dob": "2009-03-11",
            "class_name": "Grade 10-A",
            "roll_no": 11,
            "email": "vivek.rana@school.edu",
            "phone": "9890123456",
            "parent_name": "Dhiren Rana",
            "parent_phone": "9890123457",
            "address": "77 Silver Springs, Bardoli",
            "favourite_subject": "Computer",
            "attendance_pct": 88.0,
            "marks": {"Mathematics": 68, "Science": 72, "English": 74, "Computer": 85, "Social Science": 71},
            "today_status": "Present"
        },
        {
            "student_id": "STU-112",
            "full_name": "Sneha Gupta",
            "gender": "Female",
            "dob": "2009-10-19",
            "class_name": "Grade 10-A",
            "roll_no": 12,
            "email": "sneha.gupta@school.edu",
            "phone": "9901234567",
            "parent_name": "Sunil Gupta",
            "parent_phone": "9901234568",
            "address": "14 Crystal Lake, Surat",
            "favourite_subject": "Science",
            "attendance_pct": 90.0,
            "marks": {"Mathematics": 75, "Science": 89, "English": 80, "Computer": 78, "Social Science": 82},
            "today_status": "Present"
        }
    ]

    cursor = conn.cursor()
    today_str = date.today().isoformat()

    for item in sample_students:
        marks_dict = item["marks"]
        avg_marks = round(sum(marks_dict.values()) / len(marks_dict), 1)
        status = "Pass" if avg_marks >= 40.0 and all(m >= 33 for m in marks_dict.values()) else "Fail"

        cursor.execute("""
            INSERT INTO students (
                student_id, full_name, gender, dob, class_name, roll_no,
                email, phone, parent_name, parent_phone, address,
                favourite_subject, attendance_pct, average_marks, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["student_id"], item["full_name"], item["gender"], item["dob"],
            item["class_name"], item["roll_no"], item["email"], item["phone"],
            item["parent_name"], item["parent_phone"], item["address"],
            item["favourite_subject"], item["attendance_pct"], avg_marks, status
        ))

        for subj, score in marks_dict.items():
            cursor.execute("""
                INSERT INTO student_marks (student_id, subject, marks)
                VALUES (?, ?, ?)
            """, (item["student_id"], subj, score))

        cursor.execute("""
            INSERT INTO daily_attendance (student_id, date, status)
            VALUES (?, ?, ?)
        """, (item["student_id"], today_str, item["today_status"]))

    conn.commit()


def get_all_students(search_query: str = "", gender_filter: str = "All", status_filter: str = "All") -> List[Dict[str, Any]]:
    """Retrieve students matching optional search and filter criteria."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if search_query:
            query += " AND (LOWER(full_name) LIKE ? OR LOWER(student_id) LIKE ?)"
            term = f"%{search_query.strip().lower()}%"
            params.extend([term, term])

        if gender_filter and gender_filter != "All":
            query += " AND gender = ?"
            params.append(gender_filter)

        if status_filter and status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)

        query += " ORDER BY roll_no ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_student(student_id: str) -> Optional[Dict[str, Any]]:
    """Get student details by student_id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_student_marks(student_id: str) -> Dict[str, float]:
    """Get subject-wise marks for a student."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT subject, marks FROM student_marks WHERE student_id = ?", (student_id,))
        rows = cursor.fetchall()
        return {row["subject"]: row["marks"] for row in rows}


def add_student(student_data: Dict[str, Any], marks_data: Optional[Dict[str, float]] = None, today_status: str = "Present") -> bool:
    """Add a new student, their marks, and attendance for today."""
    if marks_data is None:
        marks_data = {subj: 75.0 for subj in SUBJECTS}

    avg_marks = round(sum(marks_data.values()) / max(len(marks_data), 1), 1)
    status = "Pass" if avg_marks >= 40.0 and all(m >= 33 for m in marks_data.values()) else "Fail"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (
                student_id, full_name, gender, dob, class_name, roll_no,
                email, phone, parent_name, parent_phone, address,
                favourite_subject, attendance_pct, average_marks, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_data["student_id"], student_data["full_name"], student_data["gender"],
            student_data["dob"], student_data["class_name"], student_data["roll_no"],
            student_data.get("email", ""), student_data.get("phone", ""),
            student_data.get("parent_name", ""), student_data.get("parent_phone", ""),
            student_data.get("address", ""), student_data.get("favourite_subject", "Mathematics"),
            float(student_data.get("attendance_pct", 90.0)), avg_marks, status
        ))

        for subj, mark in marks_data.items():
            cursor.execute("""
                INSERT INTO student_marks (student_id, subject, marks)
                VALUES (?, ?, ?)
            """, (student_data["student_id"], subj, mark))

        today_str = date.today().isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO daily_attendance (student_id, date, status)
            VALUES (?, ?, ?)
        """, (student_data["student_id"], today_str, today_status))

        conn.commit()
        return True


def update_student(student_id: str, student_data: Dict[str, Any], marks_data: Optional[Dict[str, float]] = None) -> bool:
    """Update existing student details and marks."""
    with get_connection() as conn:
        cursor = conn.cursor()

        if marks_data is not None:
            avg_marks = round(sum(marks_data.values()) / max(len(marks_data), 1), 1)
            status = "Pass" if avg_marks >= 40.0 and all(m >= 33 for m in marks_data.values()) else "Fail"
        else:
            current_marks = get_student_marks(student_id)
            avg_marks = round(sum(current_marks.values()) / max(len(current_marks), 1), 1) if current_marks else 0.0
            status = "Pass" if avg_marks >= 40.0 and all(m >= 33 for m in current_marks.values()) else "Fail"

        cursor.execute("""
            UPDATE students SET
                full_name = ?, gender = ?, dob = ?, class_name = ?, roll_no = ?,
                email = ?, phone = ?, parent_name = ?, parent_phone = ?, address = ?,
                favourite_subject = ?, attendance_pct = ?, average_marks = ?, status = ?
            WHERE student_id = ?
        """, (
            student_data["full_name"], student_data["gender"], student_data["dob"],
            student_data["class_name"], student_data["roll_no"], student_data.get("email", ""),
            student_data.get("phone", ""), student_data.get("parent_name", ""),
            student_data.get("parent_phone", ""), student_data.get("address", ""),
            student_data.get("favourite_subject", "Mathematics"),
            float(student_data.get("attendance_pct", 90.0)), avg_marks, status,
            student_id
        ))

        if marks_data is not None:
            cursor.execute("DELETE FROM student_marks WHERE student_id = ?", (student_id,))
            for subj, mark in marks_data.items():
                cursor.execute("""
                    INSERT INTO student_marks (student_id, subject, marks)
                    VALUES (?, ?, ?)
                """, (student_id, subj, mark))

        conn.commit()
        return True


def delete_student(student_id: str) -> bool:
    """Delete a student and all related marks & attendance records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM student_marks WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM daily_attendance WHERE student_id = ?", (student_id,))
        conn.commit()
        return True


def get_class_analytics() -> Dict[str, Any]:
    """Calculate all real-time summary statistics and chart data directly from SQLite."""
    with get_connection() as conn:
        cursor = conn.cursor()
        today_str = date.today().isoformat()

        # Total Students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        if total_students == 0:
            return {
                "total_students": 0, "present_today": 0, "absent_today": 0,
                "class_avg_marks": 0.0, "pass_students": 0, "fail_students": 0,
                "attendance_today": {"Present": 0, "Absent": 0},
                "last_exam_results": {"Pass": 0, "Fail": 0},
                "favourite_subjects": {}, "gender_distribution": {"Male": 0, "Female": 0},
                "marks_performance": [], "subject_averages": [], "attendance_comparison": []
            }

        # Attendance Today
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM daily_attendance 
            WHERE date = ? 
            GROUP BY status
        """, (today_str,))
        att_rows = dict(cursor.fetchall())
        present_today = att_rows.get("Present", 0)
        absent_today = att_rows.get("Absent", 0)
        
        # If no attendance records for today exist yet, extrapolate from students attendance_pct
        if present_today + absent_today == 0:
            cursor.execute("SELECT student_id, attendance_pct FROM students")
            for row in cursor.fetchall():
                status = "Present" if row["attendance_pct"] >= 75.0 else "Absent"
                cursor.execute("INSERT OR REPLACE INTO daily_attendance (student_id, date, status) VALUES (?, ?, ?)",
                               (row["student_id"], today_str, status))
            conn.commit()
            cursor.execute("SELECT status, COUNT(*) as count FROM daily_attendance WHERE date = ? GROUP BY status", (today_str,))
            att_rows = dict(cursor.fetchall())
            present_today = att_rows.get("Present", 0)
            absent_today = att_rows.get("Absent", 0)

        # Class Average Marks
        cursor.execute("SELECT AVG(average_marks) FROM students")
        class_avg_marks = round(cursor.fetchone()[0] or 0.0, 1)

        # Pass / Fail Students
        cursor.execute("SELECT status, COUNT(*) as count FROM students GROUP BY status")
        status_counts = dict(cursor.fetchall())
        pass_students = status_counts.get("Pass", 0)
        fail_students = status_counts.get("Fail", 0)

        # Favourite Subjects
        cursor.execute("SELECT favourite_subject, COUNT(*) as count FROM students GROUP BY favourite_subject ORDER BY count DESC")
        favourite_subjects = dict(cursor.fetchall())

        # Gender Distribution
        cursor.execute("SELECT gender, COUNT(*) as count FROM students GROUP BY gender")
        gender_distribution = dict(cursor.fetchall())

        # Marks Performance (Student-wise average marks)
        cursor.execute("SELECT student_id, full_name, average_marks, roll_no FROM students ORDER BY roll_no ASC")
        marks_performance = [
            {"student_id": row["student_id"], "name": row["full_name"], "marks": row["average_marks"], "roll_no": row["roll_no"]}
            for row in cursor.fetchall()
        ]

        # Subject Averages
        cursor.execute("SELECT subject, ROUND(AVG(marks), 1) as avg_score FROM student_marks GROUP BY subject")
        subject_averages = [{"subject": row["subject"], "average": row["avg_score"]} for row in cursor.fetchall()]

        # Attendance Comparison
        cursor.execute("SELECT student_id, full_name, attendance_pct, roll_no FROM students ORDER BY roll_no ASC")
        attendance_comparison = [
            {"student_id": row["student_id"], "name": row["full_name"], "attendance": row["attendance_pct"], "roll_no": row["roll_no"]}
            for row in cursor.fetchall()
        ]

        return {
            "total_students": total_students,
            "present_today": present_today,
            "absent_today": absent_today,
            "class_avg_marks": class_avg_marks,
            "pass_students": pass_students,
            "fail_students": fail_students,
            "attendance_today": {"Present": present_today, "Absent": absent_today},
            "last_exam_results": {"Pass": pass_students, "Fail": fail_students},
            "favourite_subjects": favourite_subjects,
            "gender_distribution": gender_distribution,
            "marks_performance": marks_performance,
            "subject_averages": subject_averages,
            "attendance_comparison": attendance_comparison
        }
