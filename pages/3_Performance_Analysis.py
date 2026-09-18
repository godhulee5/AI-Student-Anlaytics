import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import load_css

st.title("📈 Performance Analysis")

load_css()
df = pd.read_csv("student_processed.csv")

fig = px.scatter(
    df,
    x="Attendance_Pct",
    y="Final_CGPA",
    size="Study_Hours_Per_Day",
    color="Major",
    hover_data=[
        "Student_ID",
        "Previous_CGPA"
    ],
    title="Attendance vs Final CGPA"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig2 = px.scatter(
    df,
    x="Study_Hours_Per_Day",
    y="Final_CGPA",
    color="Risk_Level",
    title="Study Hours vs GPA"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)