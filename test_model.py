import joblib
import os

model_path = "models/gpa_model.pkl"

print("File exists:", os.path.exists(model_path))
print("File size:", os.path.getsize(model_path), "bytes")

print("Loading model...")

model = joblib.load(model_path)

print("SUCCESS!")
print(type(model))