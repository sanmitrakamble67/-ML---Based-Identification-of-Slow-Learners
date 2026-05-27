import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the clean data
df = pd.read_csv('student_performance_data.csv')

# Split features and target
X = df.drop('Performance_Tier', axis=1)
y = df['Performance_Tier']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, 'rf_model.pkl')
print(f"✅ Model trained successfully with exact features: {list(X.columns)}")