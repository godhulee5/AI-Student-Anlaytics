import streamlit as st
import pandas as pd
import plotly.express as px
from utils.style import load_css

st.title("📚 Major / Academic Area Analysis")

df = pd.read_csv(
    "student_processed.csv"
)

major = st.selectbox(
    "Select Major",
    sorted(df["Major"].unique())
)

filtered = df[
    df["Major"] == major
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Students",
    len(filtered)
)

col2.metric(
    "Average GPA",
    f"{filtered['Final_CGPA'].mean():.2f}"
)

col3.metric(
    "Average Attendance",
    f"{filtered['Attendance_Pct'].mean():.1f}%"
)

fig = px.histogram(
    filtered,
    x="Final_CGPA",
    title=f"GPA Distribution — {major}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
load_css()