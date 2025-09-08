# from .database.db_connection import session as db
# from .database.models import Jobs
# from sqlalchemy.dialects.postgresql import insert
from jobs.database.supabase_connection import supabase

try:
    from jobs.scrapers.Dunnitori import jobs as dunnitori_jobs
    dunnitori = dunnitori_jobs() # Today
except Exception as e:
    print(f"Error occurred while fetching Dunnitori jobs: {e}")
    dunnitori = {}


try:
    from jobs.scrapers.Jobly import jobs as jobly_jobs
    jobly = jobly_jobs() # Today
except Exception as e:
    print(f"Error occurred while fetching Jobly jobs: {e}")
    jobly = {}

try:
    from jobs.scrapers.Linkedin import jobs as linkedin_jobs
    linkedin = linkedin_jobs() # Today
except Exception as e:
    print(f"Error occurred while fetching Linkedin jobs: {e}")
    linkedin = {}

def jobs_ready_to_db():

    all_jobs = dunnitori | jobly | linkedin

    ready_jobs = []
    for job, description in all_jobs.items():
        # print (job, "location:", description.get("locations"), "link:", description.get("link"), "fi_lang:", description.get("fi_lang"), "en_lang:", description.get("en_lang"))
        # print("-"*70)
        job_in_model = {
            "title": job or None,
            "location": ', '.join(description.get("locations", None)),
            "category": description.get("category", None),
            "company": description.get("company", None),
            "link": description.get("link", None),
            "fi_lang": description.get("fi_lang", None),
            "en_lang": description.get("en_lang", None),
        }
        ready_jobs.append(job_in_model)

    response = supabase.table('jobs').upsert(ready_jobs, on_conflict='link').execute()
    print(f"Upserted {len(response.data)} jobs to Supabase.")

    ## Setup for local DB with SQLAlchemy
    
    # Test
    # job_in_model = {
    #         "title": "test",
    #         "location": "tehran",
    #         "company": None,
    #         "link": "https://example.com",
    #         "fi_lang": None,
    #         "en_lang": None,
    #     }

    # ready_jobs.append(job_in_model)


    # stmt = insert(Jobs).values(ready_jobs)
    # stmt = stmt.on_conflict_do_nothing(index_elements=['link'])

    # db.execute(stmt)
    # db.commit()

