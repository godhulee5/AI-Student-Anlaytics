import streamlit as st

st.set_page_config(
    page_title="AI Student Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Student Performance & Risk Prediction System")

st.markdown("""
### Intelligent Academic Analytics Platform

Analyze student performance, predict GPA, identify academic risk,
study attendance patterns, and compare machine learning models.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    "5,000"
)

col2.metric(
    "Average CGPA",
    "3.02"
)

col3.metric(
    "Average Attendance",
    "81%"
)

col4.metric(
    "Students at Risk",
    "214"
)

st.info(
    "Use the navigation menu on the left to explore the academic analytics system."
)

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()