import streamlit as st
import pandas as pd
import joblib
import xgboost as xgb

from utils.style import load_css


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GPA Prediction",
    page_icon="🔮",
    layout="wide"
)

load_css()


# =====================================================
# LOAD GPA MODEL
# =====================================================

@st.cache_resource
def load_gpa_model():

    # Load preprocessing
    gpa_preprocessor = joblib.load(
        "models/gpa_preprocessor.pkl"
    )

    # Load XGBoost model
    gpa_model = xgb.XGBRegressor()

    gpa_model.load_model(
        "models/gpa_xgb_model.json"
    )

    return gpa_preprocessor, gpa_model


gpa_preprocessor, gpa_model = load_gpa_model()


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "student_processed.csv"
)

df.columns = df.columns.str.strip()


# =====================================================
# TITLE
# =====================================================

st.title("🔮 GPA Prediction")

st.markdown(
    """
    Enter student academic information to predict
    the student's final CGPA using the trained
    XGBoost regression model.
    """
)

st.divider()


# =====================================================
# INPUTS
# =====================================================

col1, col2 = st.columns(2)


with col1:

    gender = st.selectbox(
        "Gender",
        sorted(
            df["Gender"]
            .dropna()
            .unique()
        )
    )


    age = st.number_input(
        "Age",
        min_value=16,
        max_value=60,
        value=21
    )


    major = st.selectbox(
        "Major",
        sorted(
            df["Major"]
            .dropna()
            .unique()
        )
    )


    attendance = st.slider(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=0.5
    )


with col2:

    study_hours = st.slider(
        "Study Hours / Day",
        min_value=0.0,
        max_value=15.0,
        value=4.0,
        step=0.5
    )


    previous_cgpa = st.slider(
        "Previous CGPA",
        min_value=0.0,
        max_value=4.0,
        value=3.0,
        step=0.01
    )


    sleep_hours = st.slider(
        "Sleep Hours / Day",
        min_value=0.0,
        max_value=15.0,
        value=7.0,
        step=0.5
    )


    social_hours = st.slider(
        "Social Hours / Week",
        min_value=0,
        max_value=80,
        value=10
    )


st.divider()


# =====================================================
# PREDICT GPA
# =====================================================

if st.button(
    "🚀 Predict GPA",
    type="primary",
    use_container_width=True
):

    # -------------------------------------------------
    # CREATE INPUT DATA
    # -------------------------------------------------

    input_data = pd.DataFrame({

        "Gender": [gender],

        "Age": [age],

        "Major": [major],

        "Attendance_Pct": [attendance],

        "Study_Hours_Per_Day": [study_hours],

        "Previous_CGPA": [previous_cgpa],

        "Sleep_Hours": [sleep_hours],

        "Social_Hours_Week": [social_hours]

    })


    # -------------------------------------------------
    # PREPROCESS INPUT
    # -------------------------------------------------

    gpa_input = gpa_preprocessor.transform(
        input_data
    )


    # -------------------------------------------------
    # PREDICT
    # -------------------------------------------------

    predicted_gpa = gpa_model.predict(
        gpa_input
    )[0]


    # Keep GPA within 0–4
    predicted_gpa = max(
        0,
        min(4, predicted_gpa)
    )


    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    st.success(
        f"Predicted GPA: {predicted_gpa:.2f} / 4.00"
    )


    # -------------------------------------------------
    # GPA INTERPRETATION
    # -------------------------------------------------

    if predicted_gpa >= 3.5:

        st.success(
            "🌟 Excellent Academic Performance"
        )

    elif predicted_gpa >= 3.0:

        st.success(
            "🟢 Very Good Academic Performance"
        )

    elif predicted_gpa >= 2.5:

        st.info(
            "🔵 Good Academic Performance"
        )

    elif predicted_gpa >= 2.0:

        st.warning(
            "🟠 Average Academic Performance"
        )

    else:

        st.error(
            "🔴 Poor Academic Performance"
        )


    # -------------------------------------------------
    # INPUT SUMMARY
    # -------------------------------------------------

    st.subheader(
        "📋 Student Information"
    )


    summary = pd.DataFrame({

        "Feature": [

            "Gender",
            "Age",
            "Major",
            "Attendance",
            "Study Hours / Day",
            "Previous CGPA",
            "Sleep Hours / Day",
            "Social Hours / Week"

        ],

        "Value": [

            gender,
            age,
            major,
            f"{attendance:.1f}%",
            f"{study_hours:.1f}",
            f"{previous_cgpa:.2f}",
            f"{sleep_hours:.1f}",
            social_hours

        ]

    })


    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )