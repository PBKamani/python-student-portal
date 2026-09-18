# 🎓 EduSoft • Student Management System

A simple, clean, and modern **Student Management System** for a small school or classroom (~10–15 students). Built using **Python**, **Streamlit**, **SQLite**, and **Plotly** with an elegant **Neumorphic / Soft UI** light design.

---

## 🌟 Highlights & Features

- **Direct Dashboard Access**: Zero authentication or login friction. The system opens directly into the live Class Dashboard.
- **Light Neumorphic / Soft UI**: Soft shadows, off-white and pale sage backgrounds, olive accents, and readable dark typography.
- **Collapsible Responsive Sidebar**:
  - **Open**: Full icons + labels (`📊 Class Data`, `👥 Students`) with collapse button.
  - **Collapsed**: Compact icon-only view (`📊`, `👥`) that expands the main viewport.
- **Class Data (Dashboard)**:
  - **6 Neumorphic KPI Cards**: Total Students, Present Today, Absent Today, Class Average Marks, Pass Count, and Fail Count.
  - **4 Distribution Donut Charts**:
    1. *Today's Attendance* (Present vs Absent)
    2. *Last Exam Result* (Pass vs Fail)
    3. *Favourite Subject Preference*
    4. *Gender Distribution* (Male vs Female)
  - **4 Analytics Charts**:
    1. *Marks Performance* (Student-by-student scores vs pass benchmark)
    2. *Subject Averages* (Class performance per subject)
    3. *Performance Trend* (Progression across roll numbers)
    4. *Attendance Comparison* (Percentage comparison with 75% cutoff line)
- **Students Management**:
  - Search by Student Name or Student ID.
  - Filter by Gender (`All`, `Male`, `Female`) and Pass/Fail status.
  - Responsive student cards displaying academic and contact details.
  - Dedicated **Individual Student Dashboard** with subject marks breakdown and attendance gauge.
- **Complete CRUD Functionality**:
  - **Create**: Add student modal (`@st.dialog`) with field validation.
  - **Read**: Live student directory and individual student dashboards.
  - **Update**: Edit modal with pre-filled student data and subject marks.
  - **Delete**: Delete modal with explicit user confirmation.
- **Dynamic SQLite Calculations**:
  - No hardcoded metrics. All summary cards and charts calculate metrics directly from `school.db`.
  - Automatically seeds 12 realistic students on the first run.

---

## 📁 Project Structure

```
student management system/
├── .streamlit/
│   └── config.toml          # Light mode theme & palette configuration
├── assets/
│   └── style.css            # Neumorphic / Soft UI custom CSS
├── database.py              # SQLite models, auto-seed data, CRUD operations & aggregations
├── app.py                   # Streamlit web application
├── test_db.py               # Unit tests verifying DB, CRUD, and analytics
├── pyproject.toml           # UV project definition
└── README.md                # Documentation and run instructions
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have `uv` installed. If not, install via:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Environment Setup & Running
Run the following commands in the project directory:

```bash
# Initialize and sync dependencies
uv sync

# Start the Streamlit application
uv run streamlit run app.py
```

Or run directly using standard Python if using an activated virtual environment:
```bash
streamlit run app.py
```

### 3. Open Application
Once running, open your web browser at:
👉 **`http://localhost:8501`**
