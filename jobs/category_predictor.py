import joblib
job_tagger = joblib.load("../job_tagger/job_tagger_pipeline.pkl")

def categorize_job(title):
    return job_tagger.predict([title])[0]
