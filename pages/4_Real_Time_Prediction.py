
import streamlit as st
import pandas as pd
import joblib
import xgboost as xgb
from pathlib import Path

from utils.style import load_css


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Real-Time Prediction",
    page_icon="⚡",
    layout="wide"
)


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "student_processed.csv"
REALTIME_FILE = BASE_DIR / "realtime_student.csv"

GPA_PREPROCESSOR_FILE = (
    BASE_DIR / "models" / "gpa_preprocessor.pkl"
)

GPA_MODEL_FILE = (
    BASE_DIR / "models" / "gpa_xgb_model.json"
)

PASS_PREPROCESSOR_FILE = (
    BASE_DIR / "models" / "pass_preprocessor.pkl"
)

PASS_MODEL_FILE = (
    BASE_DIR / "models" / "pass_xgb_model.json"
)


# =====================================================
# CSS
# =====================================================

load_css()


# =====================================================
# LOAD MODELS
# =====================================================

@st.cache_resource
def load_models():

    # GPA preprocessor
    gpa_preprocessor = joblib.load(
        GPA_PREPROCESSOR_FILE
    )

    # GPA XGBoost model
    gpa_model = xgb.XGBRegressor()

    gpa_model.load_model(
        GPA_MODEL_FILE
    )

    # Pass/Fail preprocessor
    pass_preprocessor = joblib.load(
        PASS_PREPROCESSOR_FILE
    )

    # Pass/Fail XGBoost model
    pass_model = xgb.XGBClassifier()

    pass_model.load_model(
        PASS_MODEL_FILE
    )

    return (
        gpa_preprocessor,
        gpa_model,
        pass_preprocessor,
        pass_model
    )


# =====================================================
# LOAD MODELS SAFELY
# =====================================================

try:

    (
        gpa_preprocessor,
        gpa_model,
        pass_preprocessor,
        pass_model

    ) = load_models()

except Exception as e:

    st.error(
        "❌ Error loading machine learning models."
    )

    st.exception(e)

    st.stop()


# =====================================================
# LOAD TRAINING DATA
# =====================================================

try:

    df = pd.read_csv(
        DATA_FILE
    )

    # Remove unwanted spaces from column names
    df.columns = df.columns.str.strip()

except Exception as e:

    st.error(
        "❌ Unable to load student_processed.csv"
    )

    st.exception(e)

    st.stop()


# =====================================================
# TITLE
# =====================================================

st.title(
    "⚡ Real-Time Student Prediction"
)

st.markdown(
    """
    Enter the details of a new student and the trained
    machine learning models will estimate the student's
    **Final CGPA, Pass Probability and Academic Risk**.
    """
)

st.divider()


# =====================================================
# STUDENT INFORMATION
# =====================================================

st.subheader(
    "👤 Student Information"
)

col1, col2, col3 = st.columns(3)


with col1:

    student_id = st.text_input(
        "Student ID",
        placeholder="Example: ST5001"
    )


with col2:

    gender = st.selectbox(
        "Gender",
        sorted(
            df["Gender"]
            .dropna()
            .unique()
            .tolist()
        )
    )


with col3:

    age = st.number_input(
        "Age",
        min_value=16,
        max_value=60,
        value=21,
        step=1
    )


# =====================================================
# ACADEMIC INFORMATION
# =====================================================

st.subheader(
    "📚 Academic Information"
)

col1, col2 = st.columns(2)


with col1:

    major = st.selectbox(
        "Major",
        sorted(
            df["Major"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    attendance = st.slider(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=0.5
    )

    previous_cgpa = st.slider(
        "Previous CGPA",
        min_value=0.0,
        max_value=4.0,
        value=3.0,
        step=0.01
    )


with col2:

    study_hours = st.slider(
        "Study Hours / Day",
        min_value=0.0,
        max_value=15.0,
        value=4.0,
        step=0.5
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
        value=10,
        step=1
    )


st.divider()


# =====================================================
# SAVE FUNCTION
# =====================================================

def save_prediction(prediction_data):

    new_row = pd.DataFrame(
        [prediction_data]
    )

    if REALTIME_FILE.exists():

        existing_data = pd.read_csv(
            REALTIME_FILE
        )

        existing_data.columns = (
            existing_data.columns
            .str.strip()
        )

        updated_data = pd.concat(
            [
                existing_data,
                new_row
            ],
            ignore_index=True
        )

    else:

        updated_data = new_row

    updated_data.to_csv(
        REALTIME_FILE,
        index=False
    )

    return REALTIME_FILE


# =====================================================
# PREDICTION BUTTON
# =====================================================

predict = st.button(
    "🚀 ANALYZE STUDENT",
    type="primary",
    use_container_width=True
)


# =====================================================
# REAL-TIME PREDICTION
# =====================================================

if predict:

    # -------------------------------------------------
    # VALIDATE STUDENT ID
    # -------------------------------------------------

    if not student_id.strip():

        st.warning(
            "⚠️ Please enter a Student ID."
        )

        st.stop()


    # -------------------------------------------------
    # CREATE INPUT DATAFRAME
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


    # =================================================
    # GPA PREDICTION
    # =================================================

    try:

        # Apply the SAME preprocessing used during training
        gpa_input = (
            gpa_preprocessor.transform(
                input_data
            )
        )

        # XGBoost prediction
        predicted_gpa = (
            gpa_model.predict(
                gpa_input
            )[0]
        )

        # Keep GPA between 0 and 4
        predicted_gpa = max(
            0,
            min(
                4,
                float(predicted_gpa)
            )
        )

    except Exception as e:

        st.error(
            "❌ GPA prediction failed."
        )

        st.exception(e)

        st.stop()


    # =================================================
    # PASS / FAIL PREDICTION
    # =================================================

    try:

        # Apply pass/fail preprocessing
        pass_input = (
            pass_preprocessor.transform(
                input_data
            )
        )

        # Pass/Fail prediction
        pass_prediction = (
            pass_model.predict(
                pass_input
            )[0]
        )

        # Probability of PASS
        pass_probability = (
            pass_model.predict_proba(
                pass_input
            )[0][1]
        )

        pass_probability = float(
            pass_probability
        )

    except Exception as e:

        st.error(
            "❌ Pass/Fail prediction failed."
        )

        st.exception(e)

        st.stop()


    # =================================================
    # RISK SCORE
    # =================================================

    risk_score = (

        (100 - attendance) * 0.45

        +

        (
            (4 - previous_cgpa)
            / 4
            * 100
        ) * 0.35

        +

        (
            (
                5 - min(
                    study_hours,
                    5
                )
            )
            / 5
            * 100
        ) * 0.20

    )


    # Keep between 0 and 100
    risk_score = max(
        0,
        min(
            100,
            float(risk_score)
        )
    )


    # =================================================
    # RISK LEVEL
    # =================================================

    if risk_score >= 60:

        risk_level = "High Risk"

    elif risk_score >= 35:

        risk_level = "Medium Risk"

    else:

        risk_level = "Low Risk"


    # =================================================
    # SAVE PREDICTION
    # =================================================

    prediction_data = {

        "Student_ID":
            student_id,

        "Gender":
            gender,

        "Age":
            age,

        "Major":
            major,

        "Attendance_Pct":
            attendance,

        "Study_Hours_Per_Day":
            study_hours,

        "Previous_CGPA":
            previous_cgpa,

        "Sleep_Hours":
            sleep_hours,

        "Social_Hours_Week":
            social_hours,

        "Predicted_Final_CGPA":
            round(
                predicted_gpa,
                2
            ),

        "Pass_Probability":
            round(
                pass_probability * 100,
                2
            ),

        "Pass_Fail":
            (
                "Pass"
                if int(pass_prediction) == 1
                else "Fail"
            ),

        "Risk_Score":
            round(
                risk_score,
                2
            ),

        "Risk_Level":
            risk_level
    }


    try:

        saved_file = save_prediction(
            prediction_data
        )

        st.success(
            "✅ Prediction saved successfully!"
        )

        st.caption(
            f"Saved to: {saved_file}"
        )

    except Exception as e:

        st.error(
            "❌ Prediction was calculated, "
            "but could not be saved."
        )

        st.exception(e)


    # =================================================
    # RESULTS
    # =================================================

    st.divider()

    st.subheader(
        "🤖 AI Prediction Results"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Predicted Final CGPA",
            f"{predicted_gpa:.2f} / 4.00"
        )


    with col2:

        st.metric(
            "Pass Probability",
            f"{pass_probability * 100:.1f}%"
        )


    with col3:

        st.metric(
            "Risk Score",
            f"{risk_score:.1f}%"
        )


    # =================================================
    # RISK STATUS
    # =================================================

    st.divider()

    st.subheader(
        "⚠️ Academic Risk Status"
    )


    if risk_level == "High Risk":

        st.error(
            "🔴 HIGH RISK"
        )

    elif risk_level == "Medium Risk":

        st.warning(
            "🟠 MEDIUM RISK"
        )

    else:

        st.success(
            "🟢 LOW RISK"
        )


    # =================================================
    # PASS / FAIL
    # =================================================

    st.subheader(
        "🎓 Pass / Fail Prediction"
    )


    if int(pass_prediction) == 1:

        st.success(
            f"🟢 Likely to Pass — "
            f"{pass_probability * 100:.1f}% probability"
        )

    else:

        st.error(
            f"🔴 At Risk of Failing — "
            f"{pass_probability * 100:.1f}% pass probability"
        )


    # =================================================
    # CONTRIBUTING FACTORS
    # =================================================

    st.subheader(
        "🔍 Risk Contributing Factors"
    )


    factor1, factor2, factor3 = st.columns(3)


    with factor1:

        if attendance < 75:

            st.warning(
                "⚠️ Attendance needs improvement"
            )

        else:

            st.success(
                "🟢 Attendance is satisfactory"
            )


    with factor2:

        if previous_cgpa < 2.5:

            st.warning(
                "⚠️ Previous CGPA is low"
            )

        else:

            st.success(
                "🟢 Previous CGPA is satisfactory"
            )


    with factor3:

        if study_hours < 2:

            st.warning(
                "⚠️ Low study engagement"
            )

        else:

            st.success(
                "🟢 Study engagement is satisfactory"
            )


    # =================================================
    # INPUT SUMMARY
    # =================================================

    st.divider()

    st.subheader(
        "📋 Submitted Student Information"
    )


    display_data = pd.DataFrame({

        "Feature": [

            "Student ID",

            "Gender",

            "Age",

            "Major",

            "Attendance",

            "Study Hours / Day",

            "Previous CGPA",

            "Sleep Hours",

            "Social Hours / Week"

        ],

        "Value": [

            student_id,

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
        display_data,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# REAL-TIME PREDICTION HISTORY
# =====================================================

st.divider()

st.subheader(
    "📊 Real-Time Prediction History"
)


if REALTIME_FILE.exists():

    try:

        realtime_df = pd.read_csv(
            REALTIME_FILE
        )

        realtime_df.columns = (
            realtime_df.columns
            .str.strip()
        )


        # ---------------------------------------------
        # HISTORY METRICS
        # ---------------------------------------------

        total_predictions = len(
            realtime_df
        )

        pass_count = 0

        high_risk_count = 0


        if "Pass_Fail" in realtime_df.columns:

            pass_count = (
                realtime_df["Pass_Fail"]
                .eq("Pass")
                .sum()
            )


        if "Risk_Level" in realtime_df.columns:

            high_risk_count = (
                realtime_df["Risk_Level"]
                .eq("High Risk")
                .sum()
            )


        h1, h2, h3 = st.columns(3)


        with h1:

            st.metric(
                "Total Predictions",
                total_predictions
            )


        with h2:

            st.metric(
                "Students Predicted to Pass",
                pass_count
            )


        with h3:

            st.metric(
                "High-Risk Students",
                high_risk_count
            )


        st.dataframe(

            realtime_df,

            use_container_width=True,

            hide_index=True

        )

    except Exception as e:

        st.error(
            "Unable to read realtime_student.csv"
        )

        st.exception(e)

else:

    st.info(
        "No real-time predictions have been saved yet. "
        "Run a prediction above to create the file."
    )