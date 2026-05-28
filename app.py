import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np
import random
from fpdf import FPDF
from database import SessionLocal, PredictionLog

st.set_page_config(page_title="ML - Based Identification of Slow Learners", layout="wide")
st.title("🎓 ML - Based Identification of Slow Learners")

# --- 🔒 AUTHENTICATION SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.subheader("System Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login", type="primary")
        
        if submit_button:
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()
            elif username == "student" and password == "student123":
                st.session_state.logged_in = True
                st.session_state.role = "student"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
    
    # This completely blocks the rest of the app from running if not logged in
    st.stop() 

# --- LOGOUT BUTTON (Visible on Sidebar) ---
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

st.sidebar.markdown(f"**Current User Role:** `{st.session_state.role.upper()}`")


# --- MEMORY MANAGEMENT ---
@st.cache_resource
def load_model():
    return joblib.load('rf_model.pkl')

@st.cache_data
def load_data():
    return pd.read_csv('student_performance_data.csv')

model = load_model()
df = load_data()

# Calculate Benchmarks for Advice Engine
fast_students = df[df['Performance_Tier'] == 'Fast']
benchmarks = {
    'attendance': fast_students['Attendance_%'].mean(),
    'study': fast_students['Study_Hours_Per_Day'].mean(),
    'submission': fast_students['Assignment_Submission_Rate_%'].mean()
}

# --- PDF COMPILER ---
def create_report_card(inputs, prediction, failures):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 10, "Student Performance Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"Assessed Tier: {prediction.upper()} LEARNER", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "1. Behavioral Metrics", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.cell(0, 6, f"   - Exam Score: {inputs[0]}/100", ln=True)
    pdf.cell(0, 6, f"   - Attendance: {inputs[1]}%", ln=True)
    pdf.cell(0, 6, f"   - Daily Study Time: {inputs[3]} hours", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "2. Academic Action Plan", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    if not failures:
        pdf.cell(0, 6, "   Excellent trajectory. Keep up the current habits.", ln=True)
    else:
        pdf.cell(0, 6, "   ATTENTION REQUIRED. Focus on the following gaps:", ln=True)
        for fail in failures:
            safe_fail = fail.replace("—", "-")
            pdf.multi_cell(0, 6, f"   * {safe_fail}")
            pdf.ln(2)
            
    return bytes(pdf.output())


# --- 🚦 ROLE-BASED ROUTING ---
if st.session_state.role == "admin":
    # Admins get all 4 tabs
    tab_predict, tab_eda, tab_data, tab_admin = st.tabs(["🔮 Classify & Advise", "📈 Mega EDA Dashboard", "📊 Historical Data", "🛡️ Admin Panel"])
else:
    # Students only get 1 tab
    tab_predict = st.tabs(["🔮 Classify & Advise"])[0] 
    
    # Create "invisible" tabs for the others so Python doesn't crash 
    tab_eda = st.empty()
    tab_data = st.empty()
    tab_admin = st.empty()


# --- TAB 1: PREDICTION & ADVICE (Visible to All) ---
with tab_predict:
    st.header("Enter Student Details")
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            exam = st.number_input("Exam Score (0-100)", 0, 100, 50)
            attendance = st.number_input("Attendance % (0-100)", 0, 100, 60)
            submission = st.number_input("Assignment Submission % (0-100)", 0, 100, 55)
        with col2:
            study = st.number_input("Study Hours per Day", 0.0, 24.0, 2.0, 0.5)
            cgpa = st.number_input("Previous CGPA (0-10)", 0.0, 10.0, 6.0, 0.1)
            extra = st.selectbox("Extracurricular Activities", ["Yes", "No"])

        submitted = st.form_submit_button("Predict Tier & Get Advice", type="primary", use_container_width=True)

    if submitted:
        extra_val = 1 if extra == "Yes" else 0
        
        # Gather raw features in perfect order
        raw_features = [exam, attendance, submission, study, cgpa, extra_val]
        
        # BRUTE FORCE ALIGNMENT
        input_data = pd.DataFrame([raw_features], columns=model.feature_names_in_)

        # Predict
        prediction = model.predict(input_data)[0]
        
        # Log to SQL
        try:
            db = SessionLocal()
            new_log = PredictionLog(
                exam_score=int(exam), attendance=int(attendance),
                submission=int(submission), study_hours=float(study),
                cgpa=float(cgpa), extracurricular=extra_val,
                predicted_tier=prediction
            )
            db.add(new_log)
            db.commit()
            db.close()
            st.toast("✅ Prediction securely logged to SQL database.")
        except Exception as e:
            st.error(f"Database error: {e}")

        # UI Responses
        st.markdown("---")
        if prediction == "Fast":
            st.success(f"### Predicted Tier: {prediction} Learner 🚀\nKeep up the excellent work!")
        elif prediction == "Average":
            st.info(f"### Predicted Tier: {prediction} Learner 📚\nYou are doing well, but there is room to optimize.")
        else:
            st.warning(f"### Predicted Tier: {prediction} Learner ⚠️\nLet's look at how we can get you on track.")

        # Advice Engine
        failures_for_pdf = []
        if prediction in ["Slow", "Average"]:
            st.subheader("💡 Your Personalized Action Plan")
            
            if attendance < benchmarks['attendance']:
                shortfall = int(benchmarks['attendance'] - attendance)
                msg = random.choice([
                    f"Attendance Alert: You are {shortfall}% below the top-tier average. Missing lectures creates compounding knowledge gaps.",
                    f"Action Required: Top students maintain {benchmarks['attendance']:.1f}% attendance. Make a strict rule to attend all core lectures.",
                ])
                st.error(f"**📉 {msg}**")
                failures_for_pdf.append(msg)
                
            if study < benchmarks['study']:
                gap = round(benchmarks['study'] - study, 1)
                msg = random.choice([
                    f"Study Volume: You are studying {gap} hours less than the benchmark. Implement the Pomodoro Technique.",
                    f"Time Management: Increase your daily study by {gap} hours. Break this down into two smaller blocks.",
                ])
                st.error(f"**📉 {msg}**")
                failures_for_pdf.append(msg)

        pdf_bytes = create_report_card(raw_features, prediction, failures_for_pdf)
        st.download_button(label="⬇️ Download Official Report Card (PDF)", data=pdf_bytes, file_name="Student_Report.pdf", mime="application/pdf", type="primary")


# --- TAB 2: EDA DASHBOARD (Admin Only) ---
with tab_eda:
    if st.session_state.role == "admin":
        st.header("Comprehensive Data Visualization")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.histogram(df, x="Exam_Score", color="Performance_Tier", title="Exam Score Distribution"), use_container_width=True)
        with c2:
            st.plotly_chart(px.box(df, x="Performance_Tier", y="Attendance_%", color="Performance_Tier", title="Attendance Spread by Tier"), use_container_width=True)
        
        c3, c4 = st.columns(2)
        with c3:
            st.plotly_chart(px.density_contour(df, x="Study_Hours_Per_Day", y="Exam_Score", color="Performance_Tier", title="Study vs Score Density"), use_container_width=True)
        with c4:
            st.plotly_chart(px.scatter(df, x="Study_Hours_Per_Day", y="Exam_Score", color="Performance_Tier", trendline="ols", title="Study Hours Impact"), use_container_width=True)


# --- TAB 3: DATA VIEWER (Admin Only) ---
with tab_data:
    if st.session_state.role == "admin":
        st.header("Historical Training Database")
        st.dataframe(df, use_container_width=True)


# --- TAB 4: ADMIN PANEL / SQL LOGS (Admin Only) ---
with tab_admin:
    if st.session_state.role == "admin":
        st.header("Admin Control Panel: Live AI Logs")
        try:
            db = SessionLocal()
            logs = db.query(PredictionLog).all()
            db.close()
            
            if logs:
                log_data = [{"Log ID": l.id, "Timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Exam Score": l.exam_score, "AI Prediction": l.predicted_tier} for l in logs]
                log_df = pd.DataFrame(log_data)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Evaluations", len(log_df))
                c2.metric("Fast Learners", len(log_df[log_df["AI Prediction"] == "Fast"]))
                c3.metric("At-Risk (Slow)", len(log_df[log_df["AI Prediction"] == "Slow"]))
                
                st.dataframe(log_df.sort_values(by="Log ID", ascending=False), use_container_width=True)
            else:
                st.info("No evaluations logged yet.")
        except Exception as e:
            st.error(f"Database connection failed: {e}")