from jobs.jobs_ready_to_db import jobs_ready_to_db
# from telegram import update_message

try:
    jobs_ready_to_db()
    # update_message("jobs successfully updated!")
    print("jobs successfully updated!")
except Exception as e:
    # update_message(e)
    print(f"jobs update failed: {e}")
