import streamlit as st
import pandas as pd
import plotly.express as px

from utils.style import load_css


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Attendance Analytics",
    page_icon="📅",
    layout="wide"
)

load_css()


# =====================================================
# TITLE
# =====================================================

st.title("📅 Attendance Analytics")

st.markdown(
    """
    Analyze the relationship between student attendance,
    final CGPA and academic risk.
    """
)

st.divider()


# =====================================================
# LOAD DATA
# =====================================================

try:

    df = pd.read_csv(
        "student_processed.csv"
    )

    # Remove unwanted spaces from column names
    df.columns = df.columns.str.strip()

except Exception as e:

    st.error(
        f"Unable to load student_processed.csv: {e}"
    )

    st.stop()


# =====================================================
# CHECK REQUIRED COLUMNS
# =====================================================

required_columns = [
    "Attendance_Pct",
    "Final_CGPA",
    "Risk_Level"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "Missing columns: "
        + ", ".join(missing_columns)
    )

    st.write(
        "Available columns:"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()


# =====================================================
# CLEAN DATA
# =====================================================

df["Attendance_Pct"] = pd.to_numeric(
    df["Attendance_Pct"],
    errors="coerce"
)

df["Final_CGPA"] = pd.to_numeric(
    df["Final_CGPA"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "Attendance_Pct",
        "Final_CGPA"
    ]
)


# =====================================================
# SUMMARY METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Average Attendance",
        f"{df['Attendance_Pct'].mean():.1f}%"
    )


with col2:

    st.metric(
        "Average Final CGPA",
        f"{df['Final_CGPA'].mean():.2f}"
    )


with col3:

    st.metric(
        "Highest Attendance",
        f"{df['Attendance_Pct'].max():.1f}%"
    )


with col4:

    st.metric(
        "Lowest Attendance",
        f"{df['Attendance_Pct'].min():.1f}%"
    )


st.divider()


# =====================================================
# ATTENDANCE VS GPA
# =====================================================

st.subheader(
    "📊 Attendance vs Final CGPA"
)


fig = px.scatter(

    df,

    x="Attendance_Pct",

    y="Final_CGPA",

    color="Risk_Level",

    hover_data=df.columns,

    title="Relationship Between Attendance and Final CGPA",

    labels={
        "Attendance_Pct": "Attendance (%)",
        "Final_CGPA": "Final CGPA",
        "Risk_Level": "Risk Level"
    }

)


fig.update_layout(
    height=550
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# CORRELATION
# =====================================================

correlation = df[
    [
        "Attendance_Pct",
        "Final_CGPA"
    ]
].corr().iloc[0, 1]


st.subheader(
    "📈 Attendance–GPA Correlation"
)


st.metric(
    "Pearson Correlation",
    f"{correlation:.2f}"
)


# =====================================================
# INTERPRETATION
# =====================================================

if correlation >= 0.7:

    st.success(
        "Strong positive relationship: "
        "students with higher attendance generally "
        "have higher Final CGPA."
    )

elif correlation >= 0.4:

    st.info(
        "Moderate positive relationship: "
        "attendance is associated with better "
        "academic performance."
    )

elif correlation > 0:

    st.info(
        "Weak positive relationship between "
        "attendance and Final CGPA."
    )

elif correlation <= -0.4:

    st.warning(
        "There is a negative relationship between "
        "attendance and Final CGPA."
    )

else:

    st.info(
        "There is little linear relationship between "
        "attendance and Final CGPA."
    )


# =====================================================
# RISK LEVEL DISTRIBUTION
# =====================================================

st.divider()

st.subheader(
    "⚠️ Student Risk Distribution"
)


risk_counts = (
    df["Risk_Level"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk_Level",
    "Students"
]


risk_fig = px.bar(

    risk_counts,

    x="Risk_Level",

    y="Students",

    color="Risk_Level",

    title="Students by Academic Risk Level",

    labels={
        "Risk_Level": "Risk Level",
        "Students": "Number of Students"
    }

)


risk_fig.update_layout(
    height=450
)


st.plotly_chart(
    risk_fig,
    use_container_width=True
)


# =====================================================
# ATTENDANCE CATEGORY
# =====================================================

st.divider()

st.subheader(
    "📋 Attendance Overview"
)


if "Attendance_Category" in df.columns:

    attendance_counts = (
        df["Attendance_Category"]
        .value_counts()
        .reset_index()
    )

    attendance_counts.columns = [
        "Attendance_Category",
        "Students"
    ]

    attendance_fig = px.pie(

        attendance_counts,

        names="Attendance_Category",

        values="Students",

        title="Attendance Category Distribution"

    )

    st.plotly_chart(
        attendance_fig,
        use_container_width=True
    )


# =====================================================
# DATA TABLE
# =====================================================

st.divider()

st.subheader(
    "📄 Student Attendance Data"
)


display_columns = [
    column
    for column in [
        "Student_ID",
        "Gender",
        "Major",
        "Attendance_Pct",
        "Final_CGPA",
        "Attendance_Category",
        "Risk_Level"
    ]
    if column in df.columns
]


st.dataframe(

    df[display_columns],

    use_container_width=True,

    hide_index=True

)