import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker for realistic names
fake = Faker()
np.random.seed(42)
Faker.seed(42)

n_records = 2000

# 1. Generate IDs and Names (NEW)
student_ids = range(10001, 10001 + n_records)
names = [fake.name() for _ in range(n_records)]

# 2. Base stats
exam = np.random.randint(35, 100, n_records)
cgpa = np.random.uniform(4.0, 10.0, n_records)

# 3. Behavioral variance (Noise)
attendance = np.clip(np.random.normal(75, 15, n_records), 30, 100)
submission = np.clip(np.random.normal(70, 20, n_records), 20, 100)
study = np.clip(np.random.normal(3.5, 1.5, n_records), 0.5, 8.0)
extra = np.random.choice([0, 1], n_records)

# 4. Composite score to force logic
composite_score = (exam * 0.6) + ((cgpa * 10) * 0.4)

tiers = []
for score in composite_score:
    if score >= 80:
        tiers.append('Fast')
    elif score >= 60:
        tiers.append('Average')
    else:
        tiers.append('Slow')

# 5. Build standardized dataset
df = pd.DataFrame({
    'Student_ID': student_ids,
    'Student_Name': names,
    'Exam_Score': exam,
    'Attendance_%': attendance.astype(int),
    'Assignment_Submission_Rate_%': submission.astype(int),
    'Study_Hours_Per_Day': np.round(study, 1),
    'Previous_CGPA': np.round(cgpa, 1),
    'Extracurricular_Activities': extra,
    'Performance_Tier': tiers
})

# 6. Save as BOTH CSV (for model training) and Excel (for the evaluator)
df.to_csv('student_performance_data.csv', index=False)
df.to_excel('Student_Database_Export.xlsx', index=False)

print("✅ Data generation complete!")
print("✅ Created: student_performance_data.csv")
print("✅ Created: Student_Database_Export.xlsx (Ready for Evaluator)")