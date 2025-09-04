from jobs.jobs_ready_to_db import jobs_ready_to_db
from telegram import update_message

try:
    jobs_ready_to_db()i
    update_message("jobs suseccfully updated!")
except Exception as e:
    update_message(e)
