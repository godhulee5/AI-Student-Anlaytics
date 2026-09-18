import streamlit as st
import pandas as pd

from utils.style import load_css

load_css()

st.title("👤 Student Profile")

df = pd.read_csv("student_processed.csv")

student_id = st.selectbox(
    "Select Student",
    df["Student_ID"].tolist()
)

student = df[
    df["Student_ID"] == student_id
].iloc[0]

st.subheader(f"Student: {student_id}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Attendance",
    f"{student['Attendance_Pct']:.1f}%"
)

col2.metric(
    "Previous CGPA",
    f"{student['Previous_CGPA']:.2f}"
)

col3.metric(
    "Final CGPA",
    f"{student['Final_CGPA']:.2f}"
)

col4.metric(
    "Risk",
    student["Risk_Level"]
)

st.divider()

st.write("### Academic Information")

st.dataframe(
    student.to_frame(
        "Value"
    ),
    use_container_width=True
)