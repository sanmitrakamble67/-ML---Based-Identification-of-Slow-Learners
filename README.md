# 🎓 ML-Based Identification of Slow Learners

**Live Application:** [Insert Your Streamlit Cloud URL Here]

## 📌 Project Overview
This project is a full-stack Machine Learning advisory system designed to identify and classify students into Slow, Average, or Fast Learner tiers based on academic and behavioral metrics. Moving beyond basic prediction, the system acts as an automated counselor, generating personalized academic action plans and official PDF report cards to help at-risk students get back on track.

This was developed as a Final Year Computer Science Mega Project, showcasing a complete data pipeline from synthetic data generation to model training, cloud deployment, and relational database management.

## 🚀 Core Features
* **Machine Learning Engine:** Utilizes a Scikit-Learn Random Forest Classifier (100 trees) to evaluate students based on a weighted composite of exam scores, CGPA, attendance, study habits, and assignment submission rates.
* **Dynamic Advisory System:** Automatically benchmarks at-risk students against the habits of top-tier performers and generates a personalized improvement strategy.
* **Automated PDF Reports:** Compiles the student's metrics and custom action plan into a downloadable, official PDF report card using `fpdf2`.
* **Mega EDA Dashboard:** Features a comprehensive exploratory data analysis tab with 8 interactive Plotly Express charts (histograms, box plots, density contours, and OLS trendlines).
* **Secure Admin Backend:** Logs every AI prediction and evaluation into a robust PostgreSQL database via SQLAlchemy, viewable through a protected Admin Panel.

## 🛠️ Tech Stack
* **Frontend:** Streamlit 
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
* **Database Pipeline:** PostgreSQL, SQLAlchemy, SQLite (Development)
* **Data Visualization:** Plotly Express
* **File Processing:** fpdf2 (PDF Generation), openpyxl (Excel Export)
* **Deployment:** Streamlit Community Cloud

## 📁 Repository Architecture
* `app.py`: The master frontend application containing the Streamlit UI, prediction logic, PDF compiler, and Plotly dashboards.
* `dataset.py`: A synthetic data pipeline utilizing `Faker` and `NumPy` to generate 2,000 realistic student records, exporting to both CSV (for training) and Excel (for administrative review).
* `train_model.py`: The ML training script that isolates features, fits the Random Forest model, and exports the serialized `rf_model.pkl` brain.
* `database.py`: Establishes the SQLAlchemy ORM schema and database connection architecture.
* `pg_upload.py`: A database migration script that seamlessly transfers the generated Excel data into the live PostgreSQL table.
* `requirements.txt`: Strict dependency management for cloud deployment.

## 💻 Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/sanmitrakamble67/-ML---Based-Identification-of-Slow-Learners.git](https://github.com/sanmitrakamble67/-ML---Based-Identification-of-Slow-Learners.git)
cd -ML---Based-Identification-of-Slow-Learners
