import joblib
import os

current_dir = os.path.dirname(__file__)
pickle_path = os.path.join(current_dir, "..", "job_tagger", "job_tagger_pipeline.pkl")
job_tagger = joblib.load(pickle_path)

def categorize_job(title):
    return job_tagger.predict([title])[0]
