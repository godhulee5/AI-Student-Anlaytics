import streamlit as st
import pandas as pd
import plotly.express as px

from utils.style import load_css
load_css()

st.title("📊 Student Dashboard")

df = pd.read_csv("student_processed.csv")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    len(df)
)

col2.metric(
    "Average CGPA",
    round(df["Final_CGPA"].mean(), 2)
)

col3.metric(
    "Average Attendance",
    f"{df['Attendance_Pct'].mean():.1f}%"
)

col4.metric(
    "At Risk",
    len(df[df["Risk_Level"] == "High Risk"])
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        df,
        x="Final_CGPA",
        title="GPA Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk",
        "Students"
    ]

    fig = px.pie(
        risk_counts,
        names="Risk",
        values="Students",
        title="Student Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Department / Major Performance")

major_gpa = (
    df.groupby("Major")["Final_CGPA"]
    .mean()
    .reset_index()
)

fig = px.bar(
    major_gpa,
    x="Major",
    y="Final_CGPA",
    title="Average GPA by Major"
)

st.plotly_chart(
    fig,
    use_container_width=True
)