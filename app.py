"""
Student Management System
Built with Streamlit, SQLite, and Plotly.
Neumorphic / Soft UI Light Theme.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import date, datetime

import database

# Page Configuration
st.set_page_config(
    page_title="EduSoft • Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Neumorphic Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Database & Sample Data
database.init_db()

# State Management for Navigation & Modals
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True

if "current_page" not in st.session_state:
    st.session_state.current_page = "Class Data"

if "selected_student_id" not in st.session_state:
    st.session_state.selected_student_id = None


# Soft Neumorphic Plotly Theme Colors
COLOR_PALETTE = ["#52795d", "#7ba687", "#a0c4ab", "#c7ded0", "#3a5641"]
GREEN_COLOR = "#6fa07d"
RED_COLOR = "#e57373"
FONT_FAMILY = "sans-serif"


def apply_chart_layout(fig, height=280):
    """Apply consistent Neumorphic soft UI layout to Plotly figures."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color="#25382b", size=12),
        margin=dict(l=15, r=15, t=30, b=20),
        height=height,
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=12,
            font_family=FONT_FAMILY,
            bordercolor="#d8e2da"
        )
    )
    return fig


# ---------------------------------------------------------
# MODALS & DIALOGS (Using Modern Streamlit @st.dialog)
# ---------------------------------------------------------

@st.dialog("➕ Add New Student")
def add_student_modal():
    """Dialog for adding a new student."""
    st.caption("Enter student details and initial academic marks below.")
    
    with st.form("add_student_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            # Generate suggestion for student ID
            all_stu = database.get_all_students()
            next_id = f"STU-{101 + len(all_stu)}"
            student_id = st.text_input("Student ID*", value=next_id, help="Unique identifier for student")
            full_name = st.text_input("Full Name*", placeholder="e.g. Aarav Sharma")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth*", min_value=date(2000, 1, 1), max_value=date(2020, 1, 1), value=date(2009, 5, 15))
            class_name = st.text_input("Class*", value="Grade 10-A")
            roll_no = st.number_input("Roll Number*", min_value=1, max_value=200, value=len(all_stu) + 1, step=1)
        
        with c2:
            email = st.text_input("Email", placeholder="student@school.edu")
            phone = st.text_input("Phone", placeholder="10-digit number")
            parent_name = st.text_input("Parent / Guardian Name", placeholder="Father or Mother's name")
            parent_phone = st.text_input("Parent Phone", placeholder="Guardian contact")
            address = st.text_input("Address", placeholder="City / Street")
            favourite_subject = st.selectbox("Favourite Subject*", database.SUBJECTS)
            attendance_pct = st.slider("Overall Attendance %*", min_value=0.0, max_value=100.0, value=90.0, step=1.0)
            today_status = st.selectbox("Today's Attendance*", ["Present", "Absent"])

        st.markdown("##### 📝 Subject Marks (0 - 100)")
        mc1, mc2, mc3 = st.columns(3)
        marks_dict = {}
        with mc1:
            marks_dict["Mathematics"] = st.number_input("Mathematics", 0.0, 100.0, 80.0, step=1.0)
            marks_dict["Science"] = st.number_input("Science", 0.0, 100.0, 85.0, step=1.0)
        with mc2:
            marks_dict["English"] = st.number_input("English", 0.0, 100.0, 78.0, step=1.0)
            marks_dict["Computer"] = st.number_input("Computer", 0.0, 100.0, 90.0, step=1.0)
        with mc3:
            marks_dict["Social Science"] = st.number_input("Social Science", 0.0, 100.0, 75.0, step=1.0)

        submitted = st.form_submit_button("Save Student", type="primary", use_container_width=True)
        if submitted:
            if not full_name.strip():
                st.error("Full Name is required.")
                return
            if not student_id.strip():
                st.error("Student ID is required.")
                return
            
            # Check duplicate ID
            if database.get_student(student_id):
                st.error(f"Student ID '{student_id}' already exists. Please use a unique ID.")
                return

            stu_data = {
                "student_id": student_id.strip(),
                "full_name": full_name.strip(),
                "gender": gender,
                "dob": dob.isoformat(),
                "class_name": class_name.strip(),
                "roll_no": int(roll_no),
                "email": email.strip(),
                "phone": phone.strip(),
                "parent_name": parent_name.strip(),
                "parent_phone": parent_phone.strip(),
                "address": address.strip(),
                "favourite_subject": favourite_subject,
                "attendance_pct": attendance_pct
            }

            database.add_student(stu_data, marks_dict, today_status=today_status)
            st.toast(f"✅ Student {full_name} added successfully!", icon="🎉")
            st.rerun()


@st.dialog("✏️ Edit Student Information")
def edit_student_modal(student_id: str):
    """Dialog for editing an existing student."""
    stu = database.get_student(student_id)
    if not stu:
        st.error("Student not found.")
        return

    current_marks = database.get_student_marks(student_id)
    dob_val = datetime.strptime(stu["dob"], "%Y-%m-%d").date() if stu.get("dob") else date(2009, 1, 1)

    st.caption(f"Updating profile for **{stu['full_name']}** ({stu['student_id']})")

    with st.form("edit_student_form"):
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full Name*", value=stu["full_name"])
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(stu["gender"]) if stu["gender"] in ["Male", "Female", "Other"] else 0)
            dob = st.date_input("Date of Birth*", value=dob_val)
            class_name = st.text_input("Class*", value=stu["class_name"])
            roll_no = st.number_input("Roll Number*", min_value=1, max_value=200, value=int(stu["roll_no"]), step=1)
            attendance_pct = st.slider("Attendance %*", 0.0, 100.0, float(stu["attendance_pct"]), step=1.0)
        
        with c2:
            email = st.text_input("Email", value=stu.get("email") or "")
            phone = st.text_input("Phone", value=stu.get("phone") or "")
            parent_name = st.text_input("Parent / Guardian Name", value=stu.get("parent_name") or "")
            parent_phone = st.text_input("Parent Phone", value=stu.get("parent_phone") or "")
            address = st.text_input("Address", value=stu.get("address") or "")
            fav_idx = database.SUBJECTS.index(stu["favourite_subject"]) if stu.get("favourite_subject") in database.SUBJECTS else 0
            favourite_subject = st.selectbox("Favourite Subject*", database.SUBJECTS, index=fav_idx)

        st.markdown("##### 📝 Subject Marks (0 - 100)")
        mc1, mc2, mc3 = st.columns(3)
        updated_marks = {}
        with mc1:
            updated_marks["Mathematics"] = st.number_input("Mathematics", 0.0, 100.0, float(current_marks.get("Mathematics", 75.0)), step=1.0)
            updated_marks["Science"] = st.number_input("Science", 0.0, 100.0, float(current_marks.get("Science", 75.0)), step=1.0)
        with mc2:
            updated_marks["English"] = st.number_input("English", 0.0, 100.0, float(current_marks.get("English", 75.0)), step=1.0)
            updated_marks["Computer"] = st.number_input("Computer", 0.0, 100.0, float(current_marks.get("Computer", 75.0)), step=1.0)
        with mc3:
            updated_marks["Social Science"] = st.number_input("Social Science", 0.0, 100.0, float(current_marks.get("Social Science", 75.0)), step=1.0)

        submitted = st.form_submit_button("Update Student", type="primary", use_container_width=True)
        if submitted:
            if not full_name.strip():
                st.error("Full Name cannot be empty.")
                return

            stu_data = {
                "full_name": full_name.strip(),
                "gender": gender,
                "dob": dob.isoformat(),
                "class_name": class_name.strip(),
                "roll_no": int(roll_no),
                "email": email.strip(),
                "phone": phone.strip(),
                "parent_name": parent_name.strip(),
                "parent_phone": parent_phone.strip(),
                "address": address.strip(),
                "favourite_subject": favourite_subject,
                "attendance_pct": attendance_pct
            }

            database.update_student(student_id, stu_data, updated_marks)
            st.toast("✅ Student information updated!", icon="✏️")
            st.rerun()


@st.dialog("⚠️ Confirm Deletion")
def delete_student_modal(student_id: str, student_name: str):
    """Dialog for confirming student deletion."""
    st.warning(f"Are you sure you want to delete **{student_name}** (`{student_id}`)?")
    st.caption("This action is permanent and will remove all student profile data, subject marks, and attendance history.")
    
    col_del, col_cancel = st.columns(2)
    with col_del:
        if st.button("🗑️ Yes, Delete", type="primary", use_container_width=True):
            database.delete_student(student_id)
            if st.session_state.selected_student_id == student_id:
                st.session_state.selected_student_id = None
            st.toast(f"Student {student_name} deleted.", icon="🗑️")
            st.rerun()
    with col_cancel:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

with st.sidebar:
    # Sidebar Header & Toggle
    col_t1, col_t2 = st.columns([0.7, 0.3])
    with col_t1:
        if st.session_state.sidebar_expanded:
            st.markdown("### 🎓 **EduSoft**")
            st.caption("Class Management")
        else:
            st.markdown("### 🎓")
    
    with col_t2:
        toggle_label = "◀" if st.session_state.sidebar_expanded else "▶"
        if st.button(toggle_label, key="toggle_sidebar_btn", help="Collapse / Expand Sidebar"):
            st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
            st.rerun()

    st.markdown("---")

    # Navigation choices
    if st.session_state.sidebar_expanded:
        nav_options = ["📊 Class Data", "👥 Students"]
        current_idx = 0 if st.session_state.current_page == "Class Data" else 1
        selected_nav = st.radio(
            "Navigation",
            options=nav_options,
            index=current_idx,
            label_visibility="collapsed"
        )
        if selected_nav == "📊 Class Data":
            st.session_state.current_page = "Class Data"
            st.session_state.selected_student_id = None
        else:
            st.session_state.current_page = "Students"
    else:
        nav_options = ["📊", "👥"]
        current_idx = 0 if st.session_state.current_page == "Class Data" else 1
        selected_nav = st.radio(
            "Nav",
            options=nav_options,
            index=current_idx,
            label_visibility="collapsed"
        )
        if selected_nav == "📊":
            st.session_state.current_page = "Class Data"
            st.session_state.selected_student_id = None
        else:
            st.session_state.current_page = "Students"

    st.markdown("---")
    if st.session_state.sidebar_expanded:
        st.caption("🌿 **Neumorphic Soft UI**")
        st.caption("Class 10-A • 12 Active Students")


# ---------------------------------------------------------
# VIEW: CLASS DATA (DASHBOARD)
# ---------------------------------------------------------

def render_class_data():
    """Render main Class Data dashboard with Neumorphic summary cards and Plotly charts."""
    analytics = database.get_class_analytics()

    # Top Header Banner
    st.markdown("""
        <div class="header-container">
            <div>
                <h1 class="header-title">📊 Class Overview & Analytics</h1>
                <p class="header-subtitle">Real-time academic performance, daily attendance, and student distribution for <strong>Grade 10-A</strong></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 6 Neumorphic KPI Summary Cards
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    with kpi1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-label">Total Students</div>
                <div class="kpi-value">{analytics['total_students']}</div>
                <div class="kpi-trend">Enrolled</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">✅</div>
                <div class="kpi-label">Present Today</div>
                <div class="kpi-value" style="color: #3b7c4e;">{analytics['present_today']}</div>
                <div class="kpi-trend">{round((analytics['present_today']/max(analytics['total_students'],1))*100)}% Rate</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">❌</div>
                <div class="kpi-label">Absent Today</div>
                <div class="kpi-value" style="color: #b54a4c;">{analytics['absent_today']}</div>
                <div class="kpi-trend">{analytics['total_students'] - analytics['present_today']} students</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📈</div>
                <div class="kpi-label">Class Average</div>
                <div class="kpi-value">{analytics['class_avg_marks']}%</div>
                <div class="kpi-trend">All Subjects</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-label">Passed</div>
                <div class="kpi-value" style="color: #3b7c4e;">{analytics['pass_students']}</div>
                <div class="kpi-trend">{round((analytics['pass_students']/max(analytics['total_students'],1))*100)}% Pass Rate</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi6:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">⚠️</div>
                <div class="kpi-label">Failed</div>
                <div class="kpi-value" style="color: #b54a4c;">{analytics['fail_students']}</div>
                <div class="kpi-trend">Needs Focus</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 4 Donut / Pie Charts
    st.markdown("### 🍩 Distribution Overview")
    p1, p2, p3, p4 = st.columns(4)

    # 1. Today's Attendance Pie Chart
    with p1:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📅 Today's Attendance</div>
                <div class="chart-sub">Active attendance count for today</div>
            </div>
        """, unsafe_allow_html=True)
        att_data = analytics["attendance_today"]
        fig_att = px.pie(
            names=list(att_data.keys()),
            values=list(att_data.values()),
            hole=0.6,
            color=list(att_data.keys()),
            color_discrete_map={"Present": GREEN_COLOR, "Absent": RED_COLOR}
        )
        fig_att.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        apply_chart_layout(fig_att, height=260)
        st.plotly_chart(fig_att, use_container_width=True)

    # 2. Last Exam Result Pie Chart
    with p2:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📝 Last Exam Result</div>
                <div class="chart-sub">Overall student exam outcomes</div>
            </div>
        """, unsafe_allow_html=True)
        res_data = analytics["last_exam_results"]
        fig_res = px.pie(
            names=list(res_data.keys()),
            values=list(res_data.values()),
            hole=0.6,
            color=list(res_data.keys()),
            color_discrete_map={"Pass": GREEN_COLOR, "Fail": RED_COLOR}
        )
        fig_res.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        apply_chart_layout(fig_res, height=260)
        st.plotly_chart(fig_res, use_container_width=True)

    # 3. Favourite Subject Pie Chart
    with p3:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">⭐ Favourite Subject</div>
                <div class="chart-sub">Students' preferred subjects</div>
            </div>
        """, unsafe_allow_html=True)
        fav_data = analytics["favourite_subjects"]
        fig_fav = px.pie(
            names=list(fav_data.keys()),
            values=list(fav_data.values()),
            hole=0.55,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_fav.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        apply_chart_layout(fig_fav, height=260)
        st.plotly_chart(fig_fav, use_container_width=True)

    # 4. Gender Distribution Pie Chart
    with p4:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">🧑‍🤝‍🧑 Gender Distribution</div>
                <div class="chart-sub">Class gender ratio</div>
            </div>
        """, unsafe_allow_html=True)
        gen_data = analytics["gender_distribution"]
        fig_gen = px.pie(
            names=list(gen_data.keys()),
            values=list(gen_data.values()),
            hole=0.6,
            color=list(gen_data.keys()),
            color_discrete_map={"Male": "#52795d", "Female": "#a0c4ab"}
        )
        fig_gen.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#ffffff', width=2)))
        apply_chart_layout(fig_gen, height=260)
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 4 Analytical Charts
    st.markdown("### 📊 Performance Analytics")
    c_left, c_right = st.columns(2)

    # 1. Marks Performance (Bar chart comparing students' marks)
    with c_left:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">🏆 Student Marks Performance</div>
                <div class="chart-sub">Average score per student compared against pass benchmark (40%)</div>
            </div>
        """, unsafe_allow_html=True)
        marks_df = pd.DataFrame(analytics["marks_performance"])
        if not marks_df.empty:
            marks_df["Color"] = marks_df["marks"].apply(lambda x: GREEN_COLOR if x >= 40 else RED_COLOR)
            fig_perf = go.Figure()
            fig_perf.add_trace(go.Bar(
                x=marks_df["name"],
                y=marks_df["marks"],
                marker_color=marks_df["Color"],
                text=marks_df["marks"].apply(lambda x: f"{x}%"),
                textposition="outside"
            ))
            fig_perf.add_hline(y=40, line_dash="dash", line_color="#b54a4c", annotation_text="Pass Cutoff (40%)", annotation_position="top right")
            fig_perf.update_yaxes(range=[0, 105], title="Average Marks (%)")
            fig_perf.update_xaxes(tickangle=-30)
            apply_chart_layout(fig_perf, height=310)
            st.plotly_chart(fig_perf, use_container_width=True)

    # 2. Subject Average (Bar chart showing average marks for each subject)
    with c_right:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📚 Subject Average Marks</div>
                <div class="chart-sub">Mean scores across the class per subject</div>
            </div>
        """, unsafe_allow_html=True)
        subj_df = pd.DataFrame(analytics["subject_averages"])
        if not subj_df.empty:
            fig_subj = px.bar(
                subj_df,
                x="subject",
                y="average",
                text="average",
                color="subject",
                color_discrete_sequence=COLOR_PALETTE
            )
            fig_subj.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_subj.update_yaxes(range=[0, 105], title="Mean Score (%)")
            fig_subj.update_xaxes(title="Subject")
            fig_subj.update_layout(showlegend=False)
            apply_chart_layout(fig_subj, height=310)
            st.plotly_chart(fig_subj, use_container_width=True)

    c2_left, c2_right = st.columns(2)

    # 3. Student Performance Line Chart
    with c2_left:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📈 Student Performance Trend</div>
                <div class="chart-sub">Student scores progression across roll numbers</div>
            </div>
        """, unsafe_allow_html=True)
        if not marks_df.empty:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=marks_df["name"],
                y=marks_df["marks"],
                mode="lines+markers",
                line=dict(color="#52795d", width=3),
                marker=dict(size=8, color="#3a5641"),
                name="Score"
            ))
            fig_line.add_hline(y=analytics["class_avg_marks"], line_dash="dot", line_color="#7ba687",
                               annotation_text=f"Class Mean ({analytics['class_avg_marks']}%)")
            fig_line.update_yaxes(range=[0, 105], title="Score (%)")
            fig_line.update_xaxes(tickangle=-30)
            apply_chart_layout(fig_line, height=310)
            st.plotly_chart(fig_line, use_container_width=True)

    # 4. Attendance Comparison Chart
    with c2_right:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">⏱️ Student Attendance Comparison</div>
                <div class="chart-sub">Cumulative attendance % (Warning threshold at 75%)</div>
            </div>
        """, unsafe_allow_html=True)
        att_comp_df = pd.DataFrame(analytics["attendance_comparison"])
        if not att_comp_df.empty:
            att_comp_df["Color"] = att_comp_df["attendance"].apply(lambda x: "#52795d" if x >= 75 else "#e57373")
            fig_att_comp = go.Figure()
            fig_att_comp.add_trace(go.Bar(
                x=att_comp_df["name"],
                y=att_comp_df["attendance"],
                marker_color=att_comp_df["Color"],
                text=att_comp_df["attendance"].apply(lambda x: f"{x}%"),
                textposition="outside"
            ))
            fig_att_comp.add_hline(y=75, line_dash="dash", line_color="#e57373", annotation_text="75% Minimum Requirement")
            fig_att_comp.update_yaxes(range=[0, 110], title="Attendance (%)")
            fig_att_comp.update_xaxes(tickangle=-30)
            apply_chart_layout(fig_att_comp, height=310)
            st.plotly_chart(fig_att_comp, use_container_width=True)


# ---------------------------------------------------------
# VIEW: INDIVIDUAL STUDENT DASHBOARD
# ---------------------------------------------------------

def render_student_dashboard(student_id: str):
    """Render a dedicated, detailed dashboard for a single student."""
    stu = database.get_student(student_id)
    if not stu:
        st.error("Student not found.")
        if st.button("← Back to Students List"):
            st.session_state.selected_student_id = None
            st.rerun()
        return

    marks = database.get_student_marks(student_id)

    # Back button & Actions Bar
    bar_col1, bar_col2, bar_col3 = st.columns([0.6, 0.2, 0.2])
    with bar_col1:
        if st.button("← Back to All Students", key="back_btn"):
            st.session_state.selected_student_id = None
            st.rerun()
    with bar_col2:
        if st.button("✏️ Edit Profile", key=f"dash_edit_{student_id}", use_container_width=True):
            edit_student_modal(student_id)
    with bar_col3:
        if st.button("🗑️ Delete Student", key=f"dash_del_{student_id}", use_container_width=True):
            delete_student_modal(student_id, stu["full_name"])

    # Profile Banner
    status_class = "badge-pass" if stu["status"] == "Pass" else "badge-fail"
    st.markdown(f"""
        <div class="profile-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #1e2922; font-size: 26px;">{stu['full_name']}</h2>
                    <p style="margin: 4px 0 0 0; color: #5e7364; font-size: 14px;">
                        <strong>ID:</strong> {stu['student_id']} &nbsp;•&nbsp;
                        <strong>Roll No:</strong> #{stu['roll_no']} &nbsp;•&nbsp;
                        <strong>Class:</strong> {stu['class_name']} &nbsp;•&nbsp;
                        <strong>Gender:</strong> {stu['gender']}
                    </p>
                </div>
                <div>
                    <span class="badge {status_class}" style="font-size: 14px; padding: 6px 14px;">{stu['status']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4 Quick Stat Cards
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📊</div>
                <div class="kpi-label">Average Marks</div>
                <div class="kpi-value">{stu['average_marks']}%</div>
                <div class="kpi-trend">Across 5 subjects</div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">⏱️</div>
                <div class="kpi-label">Attendance</div>
                <div class="kpi-value">{stu['attendance_pct']}%</div>
                <div class="kpi-trend">Overall Record</div>
            </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">⭐</div>
                <div class="kpi-label">Favourite Subject</div>
                <div class="kpi-value" style="font-size: 20px;">{stu['favourite_subject']}</div>
                <div class="kpi-trend">Top Interest</div>
            </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎂</div>
                <div class="kpi-label">Date of Birth</div>
                <div class="kpi-value" style="font-size: 18px;">{stu['dob']}</div>
                <div class="kpi-trend">Age ~16</div>
            </div>
        """, unsafe_allow_html=True)

    # Details & Charts Section
    d_col1, d_col2 = st.columns([0.6, 0.4])

    with d_col1:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📚 Subject-wise Marks Breakdown</div>
                <div class="chart-sub">Student scores out of 100 for each core subject</div>
            </div>
        """, unsafe_allow_html=True)
        if marks:
            marks_df = pd.DataFrame(list(marks.items()), columns=["Subject", "Marks"])
            marks_df["Color"] = marks_df["Marks"].apply(lambda x: "#52795d" if x >= 40 else "#e57373")
            fig_stu_marks = go.Figure()
            fig_stu_marks.add_trace(go.Bar(
                x=marks_df["Subject"],
                y=marks_df["Marks"],
                marker_color=marks_df["Color"],
                text=marks_df["Marks"].apply(lambda x: f"{x}"),
                textposition="outside"
            ))
            fig_stu_marks.add_hline(y=40, line_dash="dash", line_color="#e57373", annotation_text="Pass Cutoff (40)")
            fig_stu_marks.update_yaxes(range=[0, 110], title="Marks")
            apply_chart_layout(fig_stu_marks, height=290)
            st.plotly_chart(fig_stu_marks, use_container_width=True)

    with d_col2:
        st.markdown("""
            <div class="chart-box">
                <div class="chart-header">📋 Student Contact & Guardian Info</div>
                <div class="chart-sub">Personal and guardian contact details</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="inset-panel" style="font-size: 14px; line-height: 1.8;">
                <div><strong>📧 Email:</strong> {stu.get('email') or 'N/A'}</div>
                <div><strong>📞 Phone:</strong> {stu.get('phone') or 'N/A'}</div>
                <div><strong>👨‍👩‍👦 Guardian:</strong> {stu.get('parent_name') or 'N/A'}</div>
                <div><strong>📱 Guardian Contact:</strong> {stu.get('parent_phone') or 'N/A'}</div>
                <div><strong>📍 Address:</strong> {stu.get('address') or 'N/A'}</div>
            </div>
        """, unsafe_allow_html=True)

        # Mini Attendance Gauge / Indicator
        att_pct = float(stu["attendance_pct"])
        gauge_color = "#52795d" if att_pct >= 75 else "#e57373"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=att_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Attendance Status", 'font': {'size': 14, 'color': '#25382b'}},
            number={'suffix': "%", 'font': {'color': '#25382b', 'size': 24}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#25382b"},
                'bar': {'color': gauge_color},
                'bgcolor': "#e9efe9",
                'borderwidth': 1,
                'bordercolor': "#ffffff",
                'threshold': {
                    'line': {'color': "#b54a4c", 'width': 3},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        apply_chart_layout(fig_gauge, height=170)
        st.plotly_chart(fig_gauge, use_container_width=True)


# ---------------------------------------------------------
# VIEW: STUDENTS MANAGEMENT PAGE
# ---------------------------------------------------------

def render_students_page():
    """Render Student Directory with search, filters, CRUD cards, and action triggers."""
    # If a student is selected, render individual dashboard
    if st.session_state.selected_student_id:
        render_student_dashboard(st.session_state.selected_student_id)
        return

    # Header Banner with Add Student button
    h_col1, h_col2 = st.columns([0.75, 0.25])
    with h_col1:
        st.markdown("""
            <div class="header-container" style="margin-bottom: 16px;">
                <div>
                    <h1 class="header-title">👥 Student Management</h1>
                    <p class="header-subtitle">Manage student enrollment, inspect profiles, update marks, and track individual progress.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Add New Student", type="primary", use_container_width=True):
            add_student_modal()

    # Search & Filter Action Bar
    f1, f2, f3 = st.columns([0.5, 0.25, 0.25])
    with f1:
        search_query = st.text_input("🔍 Search Student", placeholder="Search by name or student ID...", label_visibility="collapsed")
    with f2:
        gender_filter = st.selectbox("Gender Filter", ["All", "Male", "Female"], label_visibility="collapsed")
    with f3:
        status_filter = st.selectbox("Status Filter", ["All", "Pass", "Fail"], label_visibility="collapsed")

    # Fetch students matching criteria
    students = database.get_all_students(
        search_query=search_query,
        gender_filter=gender_filter,
        status_filter=status_filter
    )

    st.markdown(f"<p style='color: #5e7364; font-size: 13px;'>Showing <strong>{len(students)}</strong> student(s)</p>", unsafe_allow_html=True)

    if not students:
        st.info("No students found matching the search or filter criteria.")
        return

    # Render Clean Card Grid (3 columns)
    cols = st.columns(3)
    for idx, stu in enumerate(students):
        col = cols[idx % 3]
        with col:
            status_badge = "badge-pass" if stu["status"] == "Pass" else "badge-fail"
            st.markdown(f"""
                <div class="student-card">
                    <div class="student-card-header">
                        <div>
                            <div class="student-card-name">{stu['full_name']}</div>
                            <div class="student-card-id">{stu['student_id']} • Roll #{stu['roll_no']}</div>
                        </div>
                        <div>
                            <span class="badge {status_badge}">{stu['status']}</span>
                        </div>
                    </div>
                    <div class="student-info-row">
                        <span>Class</span>
                        <strong>{stu['class_name']}</strong>
                    </div>
                    <div class="student-info-row">
                        <span>Gender</span>
                        <strong>{stu['gender']}</strong>
                    </div>
                    <div class="student-info-row">
                        <span>Avg Marks</span>
                        <strong>{stu['average_marks']}%</strong>
                    </div>
                    <div class="student-info-row">
                        <span>Attendance</span>
                        <strong>{stu['attendance_pct']}%</strong>
                    </div>
                    <div class="student-info-row">
                        <span>Favourite Subject</span>
                        <strong>{stu['favourite_subject']}</strong>
                    </div>
                    <div class="student-info-row">
                        <span>Phone</span>
                        <span>{stu.get('phone') or 'N/A'}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Action Buttons Row
            b1, b2, b3 = st.columns([0.45, 0.28, 0.27])
            with b1:
                if st.button("👁 View", key=f"view_{stu['student_id']}", use_container_width=True):
                    st.session_state.selected_student_id = stu["student_id"]
                    st.rerun()
            with b2:
                if st.button("✏️", key=f"edit_{stu['student_id']}", help="Edit Student", use_container_width=True):
                    edit_student_modal(stu["student_id"])
            with b3:
                if st.button("🗑️", key=f"del_{stu['student_id']}", help="Delete Student", use_container_width=True):
                    delete_student_modal(stu["student_id"], stu["full_name"])

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN ROUTING CONTROLLER
# ---------------------------------------------------------

if st.session_state.current_page == "Class Data":
    render_class_data()
else:
    render_students_page()
