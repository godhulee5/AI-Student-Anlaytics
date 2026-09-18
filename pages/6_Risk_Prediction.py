import streamlit as st
from utils.style import load_css

st.title("⚠️ Student Risk Prediction")

attendance = st.slider(
    "Attendance %",
    0,
    100,
    75
)

previous_gpa = st.slider(
    "Previous CGPA",
    0.0,
    4.0,
    2.8
)

study_hours = st.slider(
    "Study Hours / Day",
    0.0,
    12.0,
    4.0
)

risk_score = (
    (100 - attendance) * 0.45
    +
    ((4 - previous_gpa) / 4 * 100) * 0.35
    +
    ((5 - min(study_hours, 5)) / 5 * 100) * 0.20
)

risk_score = max(
    0,
    min(100, risk_score)
)

st.subheader("Student Risk Score")

st.progress(
    int(risk_score)
)

st.metric(
    "Risk Score",
    f"{risk_score:.1f}%"
)

if risk_score >= 60:

    st.error(
        "🔴 HIGH RISK"
    )

elif risk_score >= 35:

    st.warning(
        "🟠 MEDIUM RISK"
    )

else:

    st.success(
        "🟢 LOW RISK"
    )

st.subheader(
    "Risk Contributing Factors"
)

if attendance < 75:
    st.warning(
        "⚠️ Low attendance"
    )
else:
    st.success(
        "🟢 Attendance is satisfactory"
    )

if previous_gpa < 2.5:
    st.warning(
        "⚠️ Previous CGPA is low"
    )
else:
    st.success(
        "🟢 Previous academic performance is good"
    )

if study_hours < 2:
    st.warning(
        "⚠️ Low study engagement"
    )
else:
    st.success(
        "🟢 Study engagement is satisfactory"
    )
    
load_css()