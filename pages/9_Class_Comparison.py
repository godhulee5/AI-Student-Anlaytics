import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import load_css

st.title("👥 Class / Major Comparison")

df = pd.read_csv(
    "student_processed.csv"
)

summary = (
    df.groupby("Major")
    .agg(
        Students=("Student_ID", "count"),
        Average_GPA=("Final_CGPA", "mean"),
        Average_Attendance=("Attendance_Pct", "mean"),
        Average_Study_Hours=(
            "Study_Hours_Per_Day",
            "mean"
        )
    )
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True
)

fig = px.bar(
    summary,
    x="Major",
    y="Average_GPA",
    title="Average GPA by Major",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
load_css()